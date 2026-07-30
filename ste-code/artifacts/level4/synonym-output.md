# STE-Code Synonym Table and Output Rules

## Synonym Table (138 Pairs)

| Approved | Avoid |
|---|---|
| about | concerning, regarding, with respect to |
| add | added, adding, implement |
| administrator | admin, root, sysadmin |
| again | reoccurring |
| although | despite the fact that, even though, notwithstanding |
| analyze | analyse |
| because | as, due to the fact that, since |
| before | in advance of, preceding, prior to |
| behavior | behaviour |
| bottom | base |
| build | assemble, compile, construct, create, generate, make |
| call | dispatch, execute, fire, invoke, run, trigger |
| can | be able to, have the capability to, is capable of |
| canceled | cancelled |
| cause | induce, lead to, provoke, result in, trigger |
| center | centre |
| centralize | centralise |
| centralizes | centralises |
| change | alter, edit, modify, mutate, patch, revise, transforming, update |
| changing | mutating, transforming |
| check | assert, audit, confirm, ensure, inspect, validate, verify |
| checked | validated |
| color | colour |
| combine | aggregate, consolidate, join, merge, squash, unify |
| compile | compiling |
| connect | associate, attach, bind, join, link, wire up |
| control | direct, govern, manage, orchestrate |
| controls | determines, orchestrates |
| copies | backups |
| copy | clone, duplicate, fork, mirror, replicate, shadow |
| correct | fix, rectify, repair |
| customizable | customisable |
| customize | customise |
| decrease | diminish, lower, minimize, reduce |
| decreases | impacts |
| defect | bug, fault, flaw, issue |
| defects | bugs |
| defense | defence |
| deploy | go live, push to production, release, roll out, ship |
| detailed | comprehensive, exhaustive, verbose |
| do | carry out, execute, invoke, perform, run, trigger |
| does | running |
| duplicate | duplicated |
| examine | analyse, analyze, inspect, study |
| examines | checks |
| fail | break, crash, malfunction |
| find | detect, discover, locate, query, scan, search |
| first | initial, original, primary |
| free | deallocate, liberate, release |
| get | acquire, fetch, grab, obtain, pull, retrieve |
| gets | retrieving |
| give | ensure, furnish, hand over, provide, retourned, return, returning, supply, yield |
| gives an error | reject |
| handle | address, deal with, manage, process, take care of |
| hide | abstract away, conceal, obscure |
| if | in case of, in the event that, should it happen that |
| in | within |
| include | bundle, contain, embed, hold, nest, wrap |
| increase | boost, elevate, maximize, raise, ramp up |
| increases | raises |
| initialization | initialisation |
| initialize | initialise |
| initialized | initialised |
| initializes | initialises |
| join | combine |
| joining | combining |
| keep | cache, maintain, persist, preserve, retain, save, store |
| keeps | keeped, maintaining, persisting, stores |
| largest | biggest, greatest, maximum |
| license | licence |
| live longer than | outlive |
| log in | login |
| make | allocate, create, fabricate, generate, instantiate, produce, provision, spin up |
| make faster | optimize |
| make sure | assure, ensure, guarantee, insure |
| makes | outputting, provisions |
| makes sure | ensures |
| many | multiple, numerous, several, various |
| maximize | maximise |
| maximizes | maximises |
| meter | metre |
| minimize | minimise |
| minimizes | minimises |
| move | migrate, port, relocate, rename, shift, transfer |
| must | needs to, ought to, shall, should |
| necessary | essential, mandatory, needed, required |
| new | additional, extra, further |
| not correct | invalid, invalidating, malformed |
| operates | runs |
| optimize | optimise |
| optimizes | optimises |
| organization | organisation |
| organize | organise |
| personal | customized, personalized |
| prevent | block, disallow, forbid, prohibit, reject, stop |
| primary | base, main |
| processes | handlers |
| program | programme |
| read | fetch, import, load, obtain, pull, retrieve |
| recognize | recognise |
| recognized | recognised |
| recognizes | recognises |
| remove | delete, destroy, drop, eliminate, erase, purge, wipe |
| removes | invalidating |
| return | output, produce, respond with, send back, yield |
| run | carry out, execute, perform, runned |
| send | dispatch, forward, post, push, submit, transmit |
| sends | passes |
| serialization | serialisation |
| serialize | serialise |
| set | assign, collection, configure, declare, define, establish, setted, specify |
| sets | configuring |
| show | display, dump, output, present, print, render |
| speak to | contact, get in touch with, reach out to |
| split | break, break apart, chunk, divide, partition, separate, shard |
| standardize | standardise |
| start | bootstrap, commence, fire up, initiate, spin up |
| stop | abort, crash, halt, kill, nuke, shut down, terminate |
| stopping | crashing |
| stops | breaks, terminating |
| supplies | handlers |
| synchronize | synchronise |
| synchronizes | synchronises |
| test | check, confirm, exercise, prove, validate, verify |
| time | duration, interval, period |
| to connect again | reconnecting |
| try again | reattempt, retry, retrying |
| turn on | activate, enable, switch on |
| understand | comprehend, grasp, grok |
| unnecessary | bloat, cruft, dead code |
| update | updated |
| usage | utilisation |
| use | employ, harness, leverage, utilize |
| uses | leverages |
| when | ensure |
| with | containing, executing |
| write | assign, commit, configure, flush, persist, save, set |
| writes to the log | logs |

---

## Output Rules

### 1. Active Voice (Rule 3.6)

**Rule:** Use the active voice in all code documentation. In the active voice, the subject of the sentence performs the action. The passive voice is permitted only when the agent is genuinely unknown and cannot be substituted with "the system," "the runtime," "the compiler," or "you."

**Four methods to convert passive to active:**
1. Move the "by" agent to the subject position
2. Change an infinitive to an active verb
3. Use the imperative in procedural writing
4. Insert "you" or "we" when the agent is the reader or organization

**Test:** Every sentence must survive the test "by whom or by what?" — if an answer exists, the sentence must be rewritten with that answer as the subject.

**Examples:**
- NOT: "The API response is parsed by the middleware." → YES: "The middleware parses the API response."
- NOT: "The configuration file can be edited." → YES: "You can edit the configuration file."
- NOT: "The dependencies are installed by running `npm install`." → YES: "Install the dependencies: run `npm install`."

---

### 2. Sentence Length Rules

**Rule 5.1 — Procedural Writing (Maximum 20 Words):**
Every sentence in procedural text — installation steps, setup instructions, deployment checklists, debugging workflows, and API usage guides — must contain a maximum of 20 words. Warnings, cautions, and safety instructions must also obey the 20-word limit.

**Rule 6.3 — Descriptive Writing (Maximum 25 Words):**
Every sentence in descriptive text — README content, API reference docs, docstrings, commit messages, error messages, and inline comments — must contain a maximum of 25 words.

**Word Count Exclusions (Rule 8.6):** These elements each count as one word:
- Numbers and numbers with units of measurement (e.g., `10 ms`, `20 MB`)
- Abbreviations (e.g., `JWT`, `CI/CD`, `VPN`)
- Alphanumeric identifiers (e.g., `E36L7`, commit hashes, semantic version strings)
- Quoted text (e.g., UI labels, code snippets, formulas)
- Titles and headings
- Proper nouns (e.g., `GitHub Actions`, `Apache Software Foundation`))

**Parentheses Rule (Rule 8.5):** Text between parentheses counts as a single word in the enclosing sentence. The words inside the parentheses form their own separate sentence with its own word-count limit.

---

### 3. Imperative Mood (Rule 5.3)

**Rule:** All instructions in procedural code documentation must use the imperative (command) form. Every procedural step must start with an imperative verb such as "run," "set," "open," "save," "install," "configure," "restart," "execute," "copy," "remove," "make," "add," or "check."

**Prohibited in instructions:**
- Passive constructions ("The file can be saved")
- Modal verbs ("you can," "you should," "you may," "you could," "you might")
- Gerunds ("Saving the file...")
- Past-tense descriptions ("The script was executed")

**Notes must not use imperative** (Rule 5.5): Notes give information only, not instructions. If a note contains the imperative form, it is a work step or a safety instruction, not a note.

**Examples:**
- NOT: "The dependencies can be installed by running `npm install`." → YES: "Install the dependencies with `npm install`."
- NOT: "You can authenticate by sending a POST request." → YES: "Send a POST request."
- NOT: "Fixed the race condition." (commit message) → YES: "Fix the race condition."

---

### 4. No Contractions (Rule 4.2)

**Rule:** Contractions are prohibited in all code documentation prose. The full forms are the only approved alternatives.

**Prohibited contractions and their replacements:**
- don't → do not
- doesn't → does not
- isn't → is not
- aren't → are not
- wasn't → was not
- weren't → were not
- won't → will not
- can't → cannot
- couldn't → could not
- shouldn't → should not
- wouldn't → would not
- hasn't → has not
- haven't → have not
- hadn't → had not

**Additional No-Omission Rules (Rule 4.2):** Every sentence must have all its grammatical parts:
- Subject (no omitted subjects)
- Verb (no omitted verbs)
- Nouns (no omitted nouns)
- Articles (no omitted "the," "a," "an")

**Examples:**
- NOT: "Can accept a string or a Buffer. Returns the parsed result. Doesn't throw." → YES: "The function can accept a string or a Buffer object. The function returns the parsed result. The function does not throw an error."
- NOT: "Copy `.env.example` to `.env` and update database URL." → YES: "Copy the `.env.example` file to a `.env` file. Update the database URL in the `.env` file."

---

### 5. No Semicolons (Rule 8.1)

**Rule:** The semicolon (`;`) is not permitted in any STE-Code documentation. It enables long sentences with multiple independent clauses and has a different meaning in many programming languages (statement terminator), causing cognitive interference.

**Fix:** Split every semicolon-joined sentence into two or more independent sentences. Each sentence must stand alone with its own subject and verb.

**Examples:**
- NOT: "The server supports WebSocket connections; these use a persistent channel." → YES: "The server supports WebSocket connections. These connections use a persistent channel."
- NOT: "POST /sessions creates a new session and returns a token; the token must be included." → YES: "A POST request to /sessions makes a new session and returns a token. You must include the token."
- NOT: "Returns the user record if found; raises UserNotFoundError otherwise." → YES: "The function returns the user record when the user ID matches a database entry. The function raises a UserNotFoundError when the user ID does not match any entry."

---

### 6. No Slang or Jargon (Rule 1.10)

**Rule:** Do not use slang, jargon, or regional terms in any code documentation. Use standard, universally understood terms only. Informal verbs for failure, informal nouns for code constructs, and colloquial developer terminology are prohibited.

**Examples of prohibited jargon/slang:**
- "brick" → "make permanently unavailable"
- "blows up" → "fails"
- "nukes" → "removes"
- "tanks" → "becomes very slow"
- "eats" → "uses"
- "downstream" → "next" (when used as jargon)
- "spin up" → "make" or "start"
- "grok" → "understand"

**Rule:** Every word that has a plain-language equivalent must use that equivalent. Reserve domain-specific terminology for code identifiers (class names, function names, API endpoint names) that appear in backticks.

---

### 7. No Phrasal Verbs (Rule 9.3)

**Rule:** When you use two words together, do not make phrasal verbs. A verb and one or more prepositions together form a phrasal verb with a meaning different from the meanings of its individual parts. Replace the phrasal verb with a single approved verb.

**Common phrasal verbs to avoid:**
- "put out" → use the single verb (e.g., "emit")
- "give off" → use the single verb (e.g., "return")
- "carry out" → use the single verb (e.g., "do")
- "set up" → use the single verb (e.g., "prepare" or "configured")
- "turn on" → this IS approved as a phrasal verb in the dictionary
- "turn off" → use "stop" or "deactivate"
- "look at" → use "examine" or "see"
- "find out" → use "learn" or "discover"
- "go on" → use "continue"

**Examples:**
- NOT: "The compiler puts out a warning." → YES: "The compiler emits a warning."
- NOT: "The function gives off an error code." → YES: "The function returns an error code."
- NOT: "The cleanup task carries out deallocation." → YES: "The cleanup task does the memory deallocation."

---

### 8. Consistent Terminology (Rules 1.11 and 9.4)

**Rule 1.11 — One Term Per Concept:** Do not use different technical nouns for the same item. Use the canonical name from the most authoritative source (source code, API spec, project glossary) and apply it everywhere.

**Rule 9.4 — Consistent Style:** When you select terminology or wording, always use a consistent style. Use the same noun for the same item every time and the same verb for the same action every time.

**Rules:**
- Each concept maps to exactly one term across the entire document
- Do not alternate between synonyms (e.g., "configuration file," "settings file," "config" → pick one: "configuration file")
- Use the same verb for the same action (e.g., do not alternate between "compile," "build," and "make" for the same operation)
- Use the same grammatical structure for the same type of instruction (all endpoint docs use third-person singular, or all use imperative — pick one and stay)
- Do not abbreviate, rephrase, or alternate framework-mandated proper nouns (e.g., `ConfigMap`, `Pod`, `props`)

**Examples:**
- NOT: "Open the configuration file. Change the port in the settings file. Save the config." → YES: "Open the configuration file. Change the port in the configuration file. Save the configuration file."
- NOT: "Compile the project. Make the binary. Construct the library." → YES: "Build the project. Build the binary. Build the library."

---

### 9. Anti-Patterns (Complete List)

The following constructions are prohibited in all STE-Code documentation:

1. **Passive voice** (Rule 3.6) — unless the agent is genuinely unknown
2. **Compound verb tenses** (Rule 3.4) — present perfect (has/have + past participle), past perfect (had + past participle), future perfect (will have + past participle)
3. **"-ing" verb forms** (Rule 3.5) — progressive tenses (is building, was deploying, are processing), participial modifiers acting as verbs
4. **Nominalized verbs** (Rule 3.7) — using a noun to describe an action instead of a direct verb (e.g., "perform analysis of" → "analyze," "gives an indication of" → "shows")
5. **Omitted subjects** (Rule 4.2) — sentences without an explicit subject
6. **Omitted verbs** (Rule 4.2) — sentences without an explicit verb
7. **Omitted nouns** (Rule 4.2) — referring to code elements without naming them
8. **Omitted articles** (Rule 4.2) — missing "the," "a," "an" where they disambiguate
9. **Contractions** (Rule 4.2) — don't, isn't, won't, can't, doesn't, etc.
10. **Semicolons** (Rule 8.1) — any semicolon joining clauses, semicolons as super-commas
11. **Slang and jargon** (Rule 1.10) — informal terms, colloquial developer language, regional expressions
12. **Phrasal verbs** (Rule 9.3) — verb + preposition combinations with non-compositional meanings (unless specifically approved)
13. **Mixed-mood sentences** (Rule 4.1) — combining imperative and descriptive in one sentence
14. **Sentences with multiple instructions** (Rule 5.2) — use one instruction per sentence
15. **Multi-word nouns longer than 3 words** (Rule 2.1) — break with prepositions
16. **Nested vertical lists** (Rule 4.3) — no indented sub-lists; use a new introductory sentence
17. **Mixed imperative/descriptive items in vertical lists** (Rule 4.3) — all items must use the same grammatical form
18. **Different terms for the same concept** (Rule 1.11) — synonymy is a defect
19. **Different grammatical structures for the same type of instruction** (Rule 9.4) — all endpoint docs follow the same template
20. **Modal verbs in instructions** (Rule 5.3) — can, could, should, may, might
21. **British English spelling** (Rule 1.14) — colour, behaviour, analyse, initialise, metre, etc.
22. **Unapproved connecting words** (Rule 4.4) — however, therefore, moreover, nevertheless, consequently, furthermore
23. **Procedural sentences exceeding 20 words** (Rule 5.1)
24. **Descriptive sentences exceeding 25 words** (Rule 6.3)
25. **WARNING/CAUTION without a specific consequence** (Rule 7.3) — every safety instruction must explain the risk
26. **Abstract statements** (Rule 4.1) — "be careful," "use with caution"
27. **Using technical nouns as verbs** (Rule 1.7) — "Docker the application," "cache the result"
28. **Using technical verbs as nouns** (Rule 1.13) — "do a build of," "do a parse of"
29. **Verb forms not listed in the dictionary** (Rule 3.1) — "runned," "builded," "writed," "gived," "keeped"
30. **Parentheses for safety preconditions** (Rule 8.5) — critical information must never appear inside parentheses

---

### 10. Formatting Rules

**Vertical Lists (Rule 4.3):**
- Use a vertical list when a sentence is long and must include many different items or actions
- Put a colon at the end of the introductory sentence
- Start each list item with an uppercase letter
- Do not use commas or semicolons at item endings
- Do not mix imperative instructions with descriptive statements in the same vertical list
- Every item must connect grammatically to the introductory text
- Nested vertical lists are not permitted; use a new introductory sentence

**Colon in Vertical Lists (Rule 8.4):**
- Text before the colon obeys sentence-length limits (20 procedural, 25 descriptive)
- Each list item counts as a new sentence with its own length limit
- List items must be grammatically parallel (all noun phrases, all imperative clauses, or all full sentences)

**Paragraphs (Rules 6.4 and 6.5):**
- Each paragraph must cover only one topic
- The topic sentence is the first sentence of a paragraph
- The other sentences in the paragraph add more detail on that single topic
- When a new paragraph starts, the reader knows a new topic begins
- Reading only the topic sentences from a document should form a good outline

**Hyphens (Rule 8.2):**
- Use hyphens to connect words that are directly related in compound adjectives before nouns
- Hyphenated groups count as one word toward the multi-word noun limit
- Do not create hyphenated groups of more than three words
- Examples: "high-priority task," "read-only file descriptor," "end-to-end test," "server-side rendering"

**Parentheses (Rule 8.3):**
Permitted uses:
- References to code modules, diagrams, or related documentation
- Abbreviations introduced on first use (e.g., "Document Object Model (DOM)")
- Letters or numbers that identify items
- Singular and plural forms together (e.g., "dependency(ies)")
- Explanations of words or sentence parts
- Alternative values or configurations

Prohibited:
- Nested parentheses
- Safety preconditions inside parentheses (promote to their own sentence)

**Connecting Words and Phrases (Rule 4.4):**
Approved connecting words: "and," "but," "then," "thus"
Approved connecting phrases: "as a result," "at the same time"
Demonstrative adjectives: "this," "these" (must refer to a specific element in the previous sentence)
Unapproved connectors: "however," "therefore," "moreover," "nevertheless," "consequently," "furthermore"

**Key Words and Key Phrases (Rule 6.2):**
- Use key words (class names, function names, parameter names) to connect related ideas across sentences
- Never change key words or key phrases mid-documentation
- Use approved connecting words to show logical relationships between sentences

**Articles and Demonstrative Adjectives (Rule 4.5):**
- Use "the" before nouns that refer to a specific, identified instance
- No article before general concepts or abstract nouns
- No definite article before a noun immediately followed by a code identifier (e.g., "call function `validateInput`" not "call the function `validateInput`")
- Use "a" for first mention (indefinite), "the" for subsequent mentions (definite)

**WARNING and CAUTION Format (Rules 7.1 and 7.2):**
- Signal word in uppercase: WARNING or CAUTION
- Starts with a clear command or condition within the first few words
- WARNING: risk of security vulnerabilities, data loss, or system corruption
- CAUTION: risk of unexpected behavior, performance degradation, or incorrect results
- When both risks exist, use WARNING
- Every WARNING/CAUTION must include a specific explanation of the consequence (Rule 7.3)

**One Topic Per Sentence (Rule 6.1):**
- Each descriptive sentence contains only one subject
- Give information gradually — start with the main idea, add detail in subsequent sentences

---

### 11. Word Count Rules

**Procedural text (Rule 5.1):** Maximum 20 words per sentence

**Descriptive text (Rule 6.3):** Maximum 25 words per sentence

**Notes (Rule 5.5):** Maximum 25 words per sentence (notes are descriptive)

**Safety instructions (Rule 5.1):** Maximum 20 words per sentence

**Parenthetical text (Rule 8.5):** Text in parentheses counts as one word in the enclosing sentence and forms a separate sentence with its own length limit

**Word Count Special Handling (Rule 8.6):** Each of the following counts as ONE word:
- Numbers: `42`, `3.14`
- Numbers with units: `10 ms`, `20 MB`, `30 seconds`
- Abbreviations: `JWT`, `CI/CD`, `DOM`, `API`, `JSON`, `UUID`
- Alphanumeric identifiers: `E36L7`, `V2_3_1__migration.sql`, `1.0.0-rc1`
- Quoted text: UI labels, code snippets, terminal output, file paths in backticks
- Titles and headings
- Proper nouns: `GitHub Actions`, `Apache Software Foundation`, `Docker`

**Multi-word Nouns (Rule 2.1):** Maximum 3 words — break longer chains with prepositions

**Short Technical Nouns (Rule 1.9):** Prefer the shortest unambiguous term (maximum 3 words unless an established multi-word standard)

**One Instruction Per Sentence (Rule 5.2):** Each sentence contains only one instruction, unless two actions occur at the same time

---

### 12. American English Spelling (Rule 1.14)

**Rule:** Use American English spelling in all code documentation unless project specifications, style guides, contracts, or official directives require otherwise.

**Common British → American conversions:**
- colour → color
- behaviour → behavior
- analyse → analyze
- initialise → initialize
- organise → organize
- recognise → recognize
- utilise → utilize
- minimise → minimize
- maximise → maximize
- serialise → serialize
- synchronise → synchronize
- customise → customize
- centre → center
- metre → meter
- licence → license
- defence → defense
- cancelled → canceled

**Exception:** When quoted text (terminal output, user interface strings, error messages from third-party libraries) contains British English spelling, you must not change the spelling of the quoted text.

**Approved verb forms with American spelling:** The STE-Code dictionary specifies American English spelling for every approved word. All documentation — README files, API docs, docstrings, inline comments, headings, bullet points, and link text — must use American English.

---

### 13. Verification Checklist (10 Items)

Before publishing any code documentation, verify the following:

1. **All words are approved** (Rule 1.1): Every word in the text comes from the STE-Code controlled terminology dictionary, or is a properly registered code-domain technical noun/verb. Check the synonym table for every unapproved synonym.

2. **No contractions** (Rule 4.2): All contracted forms (don't, isn't, won't, can't, etc.) are expanded to their full forms (do not, is not, will not, cannot). Every sentence has a subject, a verb, all necessary nouns, and all necessary articles.

3. **No semicolons** (Rule 8.1): The document contains zero semicolons in prose. All semicolon-joined clauses are split into separate sentences, each with its own subject and verb.

4. **All sentences are active voice** (Rule 3.6): Every sentence names the agent that performs the action. Passive voice is only permitted when the agent is genuinely unknown. Test every sentence with "by whom or by what?"

5. **Sentence lengths are within limits** (Rules 5.1, 6.3): Procedural sentences ≤ 20 words. Descriptive sentences ≤ 25 words. Apply the word-count exceptions from Rule 8.6 for numbers, abbreviations, identifiers, quoted text, and proper nouns.

6. **All instructions are imperative mood** (Rule 5.3): Every procedural step starts with an imperative verb. No modal verbs (can, should, may, might). No passive instructions. No gerund instructions. Notes contain only descriptive text.

7. **One instruction per sentence** (Rule 5.2): No sentence contains more than one instruction (except two simultaneous actions joined by "and"). Use numbered or bulleted lists for multi-step procedures.

8. **No phrasal verbs** (Rule 9.3): Every verb+preposition combination is checked — if the combination creates a meaning different from the individual words, it is replaced with a single approved verb. Exception: phrasal verbs specifically approved in the dictionary (e.g., "turn on").

9. **Consistent terminology** (Rules 1.11, 9.4): Each code element, concept, and action has exactly one name across the entire document. No synonym switching. The same grammatical structure is used for the same type of instruction. All endpoint docs follow the same template.

10. **American English spelling** (Rule 1.14): All words use American English spelling. Check for -ise/-ize pairs, -our/-or pairs, -re/-er pairs, and -yse/-yze pairs. Quoted text from external sources is exempt from this check.

---
*Generated from STE-Code synonym-table.json v3.0.0 and 51 deepened rule files (ASD-STE100 Issue 9, January 2025, adapted to code domain)*
