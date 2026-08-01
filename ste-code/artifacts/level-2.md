# STE-Code — Level -2 (Ultra-Minimal)

The 14 core principles of STE-Code, and nothing else. Load this file when an LLM
must write or review code documentation in controlled English and you can give
it only one page.

STE-Code is a controlled-language variation of ASD-STE100 for software
documentation: README files, API references, docstrings, inline comments,
commit messages, error messages, log lines, and test descriptions.

## Scope

- The principles apply to the prose. Keep code, identifiers, command output,
  quoted strings, and error text verbatim.
- Every word in the prose must pass one of three gates:
  1. it is approved in the project controlled terminology, or
  2. it is a code-domain technical noun, or
  3. it is a code-domain technical verb.
- If a principle and clarity are in conflict, split the sentence. Do not add a
  word that is not approved.

## The 14 core principles

<!-- PRINCIPLES:START -->

### P1 — Use approved words, code-domain technical nouns, or code-domain technical verbs

Rule 1.1. Use only words that are approved in the controlled terminology, or
that are code-domain technical nouns, or that are code-domain technical verbs.
No other word is permitted.

- Write: Run the script to do the task.
- Do not write: Execute the script to do the task.

"Run" is an approved verb. "UserAuthenticator" is a code-domain technical noun.
"Serialize" is a code-domain technical verb.

Common replacements: execute → run, generate → make, configure → set,
retrieve → get, transmit → send, validate → check, utilize → use,
leverage → use, initiate → start, terminate → stop.

### P2 — Use an approved word only as its approved part of speech

Rule 1.2. Each approved word has a specified part of speech. Do not move a word
to a different part of speech.

- "Query" is an approved noun, not an approved verb. Write "Send a query to the
  database", not "Query the database".
- "Static" is an approved adjective, not a verb.
- Some words are approved as more than one part of speech. "Call" is an approved
  verb and an approved noun: "call the function", "a function call".

If the word you want is not in the controlled terminology, find the best
approved synonym, and make sure the meaning of the sentence does not change. If
the meaning changes, use a different sentence construction.

### P3 — Use an approved word only with its approved meaning

Rule 1.3. An approved word carries one approved meaning, which is often more
restricted than in standard English. Do not use a second meaning.

- The approved meaning of "run" is "execute a program or command."
- Do not write: The background worker runs every night.
- Write: The background worker operates every night.

Check each word: identify its part of speech, look up the approved meaning for
that part of speech, and ask if your sentence uses exactly that meaning. If it
does not, replace the word or rewrite the sentence.

### P4 — Use only the approved forms of verbs and adjectives

Rule 1.4. Use the approved forms only.

- COMPILE (v): compile, compiles, compiled, compiled.
- FAST (adj): fast, faster, fastest.
- Do not write "compilates" or "compilating". These forms are not approved.
- Adjectives that make comparatives with "more" and "most" keep those words,
  because "more" and "most" are approved.

### P5 — You can use words that belong to a code-domain technical noun category

Rule 1.5. A code-domain technical noun is a noun term that refers to a specified
concept in software development. The controlled terminology cannot list them
all. You can use a noun if you can put it in an approved category, for example:

- Code components, modules, and libraries: class, hook, middleware, module,
  package, plugin, repository, service.
- Computing devices and components: CPU, disk, GPU, memory, server, terminal.
- Development tools and environments: CLI, compiler, debugger, IDE, linter,
  test runner.
- Data structures, types, and formats: array, buffer, JSON, map, schema, string.

Record the technical nouns you select in the project glossary.

### P6 — Use an unapproved word only when it is part of a code-domain technical noun

Rule 1.6. A word that is not approved on its own can still be used inside a
code-domain technical noun.

- Do not write: The handler processes each incoming event.
- Write: The function processes each incoming event.
- Write: The event handler processes each incoming event. ("Event handler" is a
  code-domain technical noun.)
- Do not write: The main configuration has the latest values.
- Write: The primary configuration has the latest values.
- Write: Merge the feature branch into the main branch. ("Main branch" is a
  code-domain technical noun.)

### P7 — Do not use a code-domain technical noun as a verb

Rule 1.7. Use a technical noun only as a noun, or as an adjective inside another
technical noun. Change the sentence construction instead.

- Do not write: Database the user records before the migration.
- Write: Store the user records in the database before the migration.
- Do not write: Cache the API responses.
- Write: Put the API responses in the cache.

### P8 — Use the code-domain technical nouns that your project approves

Rule 1.8. If your project, company, industry, or subject field has an approved
name for a class, module, function, variable, component, or process, use that
name. Take the name from the code itself and from the project glossary, API
documentation, or coding standards. Do not invent a new name for an item that
already has one.

### P9 — Select a technical noun that is short and easy to understand

Rule 1.9. When no approved technical noun exists, select one that is short (not
more than three words) and easy to understand. Do not write a long descriptive
phrase when a short term is sufficient. If the term needs clarification, add one
or two adjectives.

### P10 — Do not use regional, slang, or jargon words as technical nouns

Rule 1.10. Some words are known only inside one community or one technology
stack. Code documentation is read by junior developers, by developers from other
ecosystems, and by readers whose first language is not English. Select well-known
words only.

- Do not write: Yeet the stale records from the cache.
- Write: Delete the stale records from the cache.
- Do not write: The build is borked.
- Write: The build failed.

### P11 — Do not use different technical nouns for the same item

Rule 1.11. Use one name for one item through all of the documentation. If you
call it "the auth service" in one section, do not call it "the login server" in
another. The source of truth is the code: the class, function, module, table,
resource, environment variable, or configuration key as it is defined in the
repository.

### P12 — You can use verbs that belong to a code-domain technical verb category

Rule 1.12. A code-domain technical verb refers to a specified operation or
process in software development. You can use a verb if you can put it in an
approved category, for example:

- Development processes: compile, import, lint, refactor, transpile; assert,
  benchmark, debug, mock, profile; bundle, deploy, package, publish, release;
  install, pin, update, upgrade.
- Computer processes and applications: cache, index, parse, query, render,
  serialize, sort, validate.

A code-domain technical verb must obey the same rules as any other approved
verb.

### P13 — Do not use a code-domain technical verb as a noun

Rule 1.13. Use a technical verb only as a verb. If you need a noun, use an
approved noun or a technical noun with the same meaning.

- Do not write: Do a build of the project.
- Write: Build the project.
- Do not write: The function does a parse of the input string.
- Write: The function parses the input string.
- Do not write: Compile of module "auth" failed.
- Write: Failed to compile module "auth".

Commit messages use the imperative: "Add login endpoint", not "Addition of login
endpoint". When the API returns a named artifact (a `Build` object, a
`Deployment` resource), the noun is a technical noun and is correct.

### P14 — Use American English spelling

Rule 1.14. Use the American English spelling given in the controlled
terminology. Use a different spelling only when a project specification, style
guide, contract, or other official directive tells you to.

- Write: initialize, serialize, behavior, color, catalog.
- Do not write: initialise, serialise, behaviour, colour, catalogue.

Do not change the spelling inside quoted text. If an error message, a code
comment, or a user interface string uses British spelling, keep it as it is.

<!-- PRINCIPLES:END -->

## Checklist

Before you publish, check each sentence:

1. Is every word approved, a code-domain technical noun, or a code-domain
   technical verb? (P1)
2. Is every word used as its approved part of speech (P2) and with its approved
   meaning (P3), in an approved form (P4)?
3. Are technical nouns taken from a category (P5, P6), kept as nouns (P7), taken
   from the project (P8), and short (P9)?
4. Is the vocabulary free of slang (P10) and consistent for each item (P11)?
5. Are technical verbs taken from a category (P12) and kept as verbs (P13)?
6. Is the spelling American English outside of quoted text? (P14)

## Next level

Level -1 gives the same principles with the writing rules for sentences,
procedures, and descriptive text. Level 0 adds the baseline rule set. Higher
levels add the dictionary, the grammar rules, and the code-domain extensions.

