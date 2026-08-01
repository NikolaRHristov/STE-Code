# Level 4 — Section 5: Procedural Sentence Rules

Section 5 controls how you write the sentences of a *procedure* in code
documentation: setup steps, runbooks, API usage guides, commit messages,
debugging playbooks, and inline how-to comments.

Five rules, one idea: **every procedural sentence is short, carries one
instruction, uses the imperative form, states any condition first, and keeps
background in notes — not in the steps.**

| Rule | Statement | Watch for |
|---|---|---|
| 5.1 | Write short sentences (maximum 20 words). | Sentences over 20 words; comma splices; semicolons joining clauses |
| 5.2 | Write only one instruction per sentence. | Several actions joined by "and"/"then" in one sentence |
| 5.3 | Write instructions in the imperative (command) form. | Passive voice, modal verbs, gerunds used as instructions |
| 5.4 | Put the condition before the command, separated by a comma. | Conditions buried after the action; misplaced commas |
| 5.5 | Notes give information only, not instructions. | Instructions, requirements, or limits hidden inside a NOTE |

Scope: these rules apply to *procedural text*. Code blocks, terminal output,
string literals, and identifiers inside backticks are not counted. Notes and
descriptive sentences have a 25-word-per-sentence limit; procedural sentences
have a 20-word limit.

## Word-count basis (applies to 5.1 and 5.5)

- Count all words from the initial capital to the terminal punctuation.
- A hyphenated compound ("command-line") counts as one word.
- A number, symbol, or parenthetical reference counts as one word: "(2)" = 1,
  "HTTP/2" = 1.
- A code token inside backticks counts as one word regardless of length:
  `Result<T, E>` = 1 word, `async fn` = 2 words. Do not expand generics or
  type parameters into prose words.
- Subordinate-clause depth: limit to two levels. Flatten deeper embeddings into
  separate sentences.

## Rule 5.1 — Short Sentences (Maximum 20 Words)

Keep every sentence in a procedure to 20 words or fewer. Warnings and cautions
about security, data loss, or stability also obey the 20-word limit. Notes may
use up to 25 words per sentence because they carry information only.

Break long procedural sentences into shorter ones, each focusing on one part of
the task. This matters most when the reader types commands while reading.

Code-domain examples:

- Non-STE (27 w): Run the database migration script from the project root
  directory and then restart the application server to apply all pending schema
  changes to the production environment.
- STE (9 + 13 w): Run the database migration script from the project root
  directory. Then, restart the application server to apply all pending schema
  changes.
- Non-STE (30 w): Set the environment variable HTTP_TIMEOUT to the value 30000
  which represents the maximum number of milliseconds that the client will wait
  for a response from the upstream server.
- STE (8 + 17 w): Set the environment variable HTTP_TIMEOUT to 30000. This value
  is the maximum wait time in milliseconds for a response from the upstream
  server.

```bash
alembic upgrade head
systemctl restart payments.service
export HTTP_TIMEOUT=30000
```

CAUTION (18 w): IF YOU DELETE THE CONFIGURATION DIRECTORY WITHOUT A BACKUP, YOU
CANNOT RESTORE THE APPLICATION SETTINGS TO THEIR PREVIOUS STATE.

### Where this applies in code docs

- **README** — each install/config/quick-start step is one ≤20-word sentence.
- **API docs** — request/setup sentences obey 20 words; descriptive parameter
  prose may use 25.
- **Docstrings** — procedural sentences in a docstring obey 20 words; return
  value/side-effect descriptions may use 25.
- **Commit bodies** — procedural sentences obey 20 words; subject line is a
  separate 72-character constraint, not a word-count one.
- **Error messages** — action messages obey 20 words; pure status reports may
  use 25 (read under stress, keep short).

### How to split a long sentence

1. **Split at coordinating conjunctions** — replace "and"/"but"/"or" with a
   period; start the next sentence with "Then,"/"After that,"/"Next."
2. **Extract conditions** — move an "if X, then Y" clause into its own sentence
   that precedes or follows the instruction.
3. **Separate action from purpose** — instruction in one sentence, reason/result
   in the next.
4. **Use lists** — enumerate items as bullets; list items are not sentences and
   are exempt, but keep each item short.

**Coordinating-conjunction policy:** "and"/"but"/"or" may join two short related
clauses only when the total is ≤20 words. If over 20, split at the conjunction.

**Run-on / semicolon policy:** do not join independent clauses with semicolons.
Use periods. Each instruction gets its own sentence.

**Subordinate depth:** three or more levels of embedding is hard to parse and
usually over 20 words. Promote embedded clauses to their own sentences.

### Edge cases

- **Long framework/service names** — use the shortest accepted form on first
  use, define an abbreviation, then reuse it (e.g. "Amazon EKS" → "EKS"). The
  abbreviation counts as one word.
- **Generated docs** — apply the rule to the source docstrings/comments the
  generator reads; the output inherits compliance. If a generator cannot comply
  from compliant input, file a bug against the generator; do not hand-edit
  generated output. If fixing the source is impractical, apply the 25-word
  descriptive limit and document the exception.
- **Legal/compliance text** — disclaimers, license headers, and regulatory
  statements are not procedures; the 20-word limit does not apply. Keep them in a
  marked section (NOTE / "Legal" heading) separate from steps.
- **Code blocks in prose** — a sentence that introduces a multi-line code block
  must obey the limit on its own; the block itself is excluded from the count.

### Compliance checklist (5.1)

- [ ] Every procedural sentence ≤ 20 words.
- [ ] Every note sentence ≤ 25 words.
- [ ] Warnings/cautions ≤ 20 words.
- [ ] No comma splices (no two independent clauses joined by a comma).
- [ ] No semicolons joining independent clauses.
- [ ] Code blocks, output, and string literals excluded from counts.
- [ ] Backtick code tokens count as one word each.
- [ ] Long technical names abbreviated after first definition.
- [ ] Subordinate clauses ≤ two levels deep.
- [ ] Conjunctions join two clauses only when total ≤ 20 words.

## Rule 5.2 — One Instruction Per Sentence

Write only one instruction in each sentence unless two or more actions occur at
the same time and in one continuous motion. If a sentence carries several
instructions, the reader can miss or skip one. Use numbered or bulleted lists to
show the sequence of steps. There is no limit on the number of work steps.

Code-domain examples:

- Non-STE (37 w, 5 instructions): Open the configuration file in a text editor
  and locate the database section and change the connection string to point to
  the staging server and then save the file and close the editor.
- STE: (1) Open the configuration file in a text editor. (2) Locate the database
  section. (3) Change the connection string to point to the staging server.
  (4) Save the file. (5) Close the editor.

```markdown
1. Open `config/database.toml` in a text editor.
2. Find the `[database]` section.
3. Set `connection_string = "postgres://staging-db:5432/app"`.
4. Save the file.
5. Close the editor.
```

Exceptions — more than one instruction is allowed when:

- Two or more actions occur at the same time and are inseparable (hold Shift and
  click Reload; download and extract the archive).
- A result or measurement follows an action immediately, and splitting it would
  break the logical flow (one action: "Run the full test suite with coverage
  enabled. The total line coverage must be more than 80 percent.").

### Where this applies

- **README** — every numbered quick-start/install step is exactly one
  instruction; a result that must be checked is a second sentence in the same
  step.
- **API docs** — one sentence per endpoint operation; one sentence per parameter,
  per query param, per response field, per error code.
- **Docstrings** — one sentence per parameter, per return value, per raised
  exception, per side effect/precondition.
- **Commit subjects** — one imperative sentence, one change. Split the commit if
  changes are unrelated; use body bullets for related changes.
- **Error messages** — state one problem, give one action; do not combine
  failure paths with "or"/"and"/"also".

### Paradigm notes

- **OOP** — document each constructor parameter in its own sentence; number each
  step of a multi-step setup; do not chain method calls in one prose sentence.
- **Functional** — describe each pipeline stage (map/filter/reduce) in its own
  sentence; do not combine stages into one explanatory sentence.
- **Procedural (C/Go/Bash)** — one comment per executable statement; put the
  comment on the line before the command.
- **Declarative (SQL/Terraform/K8s)** — one sentence per resource, property, and
  constraint.
- **Systems (Rust ownership/C memory)** — state each invariant in its own
  sentence.

### Grammar notes

- **Single predicate** — an imperative sentence has exactly one main verb:
  "Install the package." (not "Install the package and configure the settings.").
- **Compound objects are not compound instructions** — "Remove the log files,
  cache files, and temporary directories." is one instruction (one verb, three
  objects).
- **"-ing" prohibition** — gerunds blur action/description and smuggle in hidden
  instructions; split them into numbered steps.
- **Subordinate clause test** — if the reader must satisfy a precondition in a
  subordinate clause, that precondition is itself an instruction and needs its
  own step: "Before you run the tests, set TEST_MODE=true." → (1) Set
  TEST_MODE=true. (2) Run the tests.

### Edge cases

- **Framework CLI names** — `docker compose up`, `kubectl apply`,
  `terraform destroy` are one technical noun phrase (Rule 1.5). Do not split the
  command name into separate instructions.
- **Error messages with cascading symptoms** — state the root cause first; list
  consequences in a separate descriptive sentence.
- **Multi-step test assertions** — describe each assertion in its own sentence;
  use one assertion message per condition.
- **Console logs during multi-step ops** — each log line reports one completed
  step or one result.

## Rule 5.3 — Imperative (Command) Form for Instructions

Write every instruction in the imperative (command) form: start the sentence
with the base verb. Common imperative verbs in code docs: run, set, open, save,
install, configure, restart, execute, copy, delete, create, add, enter, select,
click, type, check.

Do not use passive voice, gerunds, or modal verbs (can, could, should, may,
might) for instructions. Do not use "must" before the imperative in a standard
instruction. Reserve "must" for WARNING/CAUTION blocks where non-compliance is
severe.

Code-domain examples:

- Non-STE: The unit tests can be executed with the command `npm test`.
- STE: Run the unit tests with the command `npm test`.
- Non-STE: The old log files are to be removed before the new deployment.
- STE: Remove the old log files before the new deployment.
- Non-STE: It is recommended that you create a backup of the database before
  running the migration script.
- STE: Create a backup of the database before you run the migration script.

WARNING (correct use of "must"): IF YOU MUST STORE USER PASSWORDS, ALWAYS HASH
THEM WITH BCRYPT. DO NOT STORE PASSWORDS IN PLAIN TEXT. PLAIN-TEXT PASSWORDS CAN
CAUSE DATA BREACHES.

### Where the imperative form applies

- **README** — only procedural sections (install, config, build, quick-start).
  Descriptive sections (about, architecture, features) use declarative sentences.
- **API docs** — only setup/auth/getting-started instructions. Endpoint
  descriptions are third-person ("Returns a list of users") because they describe
  behavior.
- **Docstrings** — describe what the code does (declarative). Exception: shell
  script headers and Makefile targets that the reader runs directly.
- **Commit subjects** — imperative ("Fix the race condition"), matching Git's own
  convention. Bodies may use descriptive sentences for rationale.
- **Error messages** — describe what happened, then give a recovery instruction;
  separate with a period or newline.

### Grammar notes

- **Subject omission** — the imperative omits "you"; the reader is always the
  implied subject. Passive hides the agent ("The file is saved" — who saves it?).
- **Modal verb elimination** — "You can set the timeout" lets the reader treat
  the action as optional; "Set the timeout" does not.
- **"must" restriction** — imperative already conveys necessity; "must" is
  redundant except in WARNING/CAUTION.
- **Tense consistency** — the base verb form does not inflect; this eases
  translation and machine processing.

### Paradigm notes

- **OOP** — imperative for setup/config instructions; declarative for invariants
  and design rationale.
- **Functional** — imperative for build/REPL/setup; declarative for what a
  function does internally.
- **Procedural (C/Go/Bash)** — imperative dominates (build, compile, link,
  configure).
- **Declarative (SQL/Terraform/K8s)** — imperative only for the tooling that
  applies the state (`kubectl apply`, pipeline steps); the spec itself is
  descriptive.
- **Systems** — imperative in "how to comply" sections; descriptive for
  invariants and lifetimes.

### Edge cases

- **Framework name = verb** (React, Spring, Go, Make) — do not start a sentence
  with the name; prefix with an article or use a real verb: "Use React to build
  the UI." (not "React to state changes with hooks.").
- **Generated help/changelog text** — audit the generator template, not the
  output: `--help` text "Write the output to this file" (not "The output file is
  written here"); changelog "Add support for OAuth2" (not "Added support for
  OAuth2").
- **Code keywords that are English modals** (`try`, `await`, `yield`, `require`)
  — backtick them; do not start an imperative sentence with the keyword unless it
  is the verb: "Use `await` on the promise before you access the result."
- **Release notes** — imperative for upgrade/migration steps; past/present
  perfect for feature/bugfix descriptions.
- **Interactive tutorials** — label blocks clearly ("Run this command" vs "You
  will see output like this"); keep the imperative in the step labels.

## Rule 5.4 — Descriptive Statement Before the Command

When a step has a condition the reader must know first, write the condition as a
descriptive statement at the start of the sentence, then a comma, then the
instruction in the imperative form. The comma is mandatory: it marks where the
condition scope ends and the command scope begins.

The comma's position changes meaning. Compare:

- "If the service does not start, automatically restart it." (the restart is
  automatic)
- "If the service does not start automatically, restart it." (the reader restarts
  it manually)

Code-domain examples:

- Non-STE: Run the database migration script after you set DATABASE_URL to your
  production connection string and confirmed the server accepts connections.
- STE: After you set the `DATABASE_URL` environment variable, run the database
  migration script.
- Non-STE: You can call /users after you obtain a valid OAuth2 token and include
  it in the Authorization header.
- STE: After you get a valid OAuth2 access token from `/auth/token`, call the
  `/users` endpoint. Include the token in the `Authorization` header.
- Non-STE: The API returns 429 with a Retry-After header if the client exceeds
  100 requests per minute.
- STE: If the client sends more than 100 requests per minute, the API returns a
  `429 Too Many Requests` status code. The response includes a `Retry-After`
  header that shows the wait time.

### Where this applies

- **README** — one condition-command pair per step; do not chain several
  conditions in one sentence.
- **API docs** — state the error-triggering condition before the response; gate
  requests on a prerequisite token.
- **Docstrings** — state preconditions before behavior (precondition-before-
  action).
- **Commit messages** — context/problem before the fix (context-before-action).
- **Error messages** — problem before resolution; each corrective action is its
  own condition-command pair.

### Paradigm notes

- **OOP** — state preconditions on method calls before the call instruction; for
  constructors, state the required initial state.
- **Functional** — state the input condition before the transformation; treat
  each guard/pattern branch as a separate condition-result pair.
- **Procedural (C/Go/Bash)** — state the system-state check before the action;
  shell `if` maps directly to the condition clause.
- **Declarative (SQL/Terraform/K8s)** — apply the pattern to the operational
  wrapper (how to apply/run), not to the declarative spec itself.
- **Systems** — state safety conditions before the operation; use WARNING/BREAKING
  when the consequence is severe.

### Grammar notes

- **Comma as scope delimiter** — required, not optional. The reader's eye scans
  for it; it signals the transition from evaluation to action.
- **Adverb placement** — `[condition] , [adverb] [command]` → adverb modifies
  the command. `[condition with adverb] , [command]` → adverb modifies the
  condition. When both need an adverb, use two sentences.
- **Dependent-clause types** — time (before/after/when/until), conditional
  (if/unless/provided that), reason (because), purpose (to/in order to),
  concessive (although). Each dependent clause comes first, comma, then main
  clause. Do not reverse the order.
- **Multiple conditions** — prefer separate sentences (Strategy C): "Before you
  run the migration, make sure the server is running. After the server accepts
  connections, run the migration script." A compound "and" condition is
  acceptable only when short.
- **Works with 5.3** — pattern: `[condition clause] , [imperative verb] [object]`.
  The comma bridges the descriptive condition and the imperative command.

### Edge cases

- **Framework name = common word** (Next.js, Express) — the name is a technical
  noun; the comma-after-condition rule still applies: "Before you start the
  Next.js development server, set the environment variables."
- **Code keyword inside the condition** — the comma goes after the closing
  backtick: "If `response.status === 429`, wait for the duration in the
  `Retry-After` header."
- **Condition clause has its own commas** (an internal list) — restructure.
  Either introduce the list in a separate descriptive sentence, then use a
  comma-free condition ("If you change one or more of these parts, update the
  version number."), or keep the pattern only when the condition has at most one
  internal comma.
- **Condition implied by tool output** — state the observable output as the
  condition: "If the terminal shows 'Connection refused,' start the database
  server."
- **Generated docs** — relax for generated output, but keep Rule 5.4 in the
  source docstring/comment; for templates, place the condition placeholder first.

## Rule 5.5 — Notes Give Information Only, Not Instructions

A NOTE gives supplementary information that helps the reader understand context,
behavior, or background. A note must contain descriptive information only. It
must not contain instructions, requirements, limits, tolerances, or expected
results of a work step. Notes must not use the imperative form. Each sentence in
a note can have up to 25 words.

If a note holds information critical for preventing data loss, security issues,
or system damage, move it into a WARNING or CAUTION safety instruction. A note is
never a substitute for a safety instruction.

**The note test:** read the procedure without the notes. If the reader cannot do
the procedure correctly, move the missing information from the notes into work
steps and repeat the test.

Code-domain examples:

- STE note (descriptive only): NOTE: The API rate limiter allows a maximum of
  1000 requests per minute per client IP address on the free tier.
- Non-STE (instruction in a note): NOTE: When you update the dependencies, run
  `npm audit fix` to resolve known vulnerabilities.
- STE (instruction → work step): (5) Run the command `npm audit fix` to resolve
  known vulnerabilities.
- Non-STE (limit in a note): NOTE: The response time must be less than 200 ms
  under normal load.
- STE (limit → in the endpoint body, not a note): The response time must be less
  than 200 milliseconds under normal load conditions.
- Non-STE (safety in a note): NOTE: Do not run the migration on production without
  a full backup.
- STE (safety → WARNING): WARNING: DO NOT RUN THE MIGRATION SCRIPT ON THE
  PRODUCTION DATABASE WITHOUT A FULL BACKUP. RUNNING THE MIGRATION WITHOUT A
  BACKUP CAN CAUSE IRREVERSIBLE DATA LOSS.

### Where this applies

- **README** — notes explain why a dependency exists or a design decision; they
  do not install packages or run commands (those are numbered steps).
- **API docs** — notes explain behavior, side effects, constraints; they do not
  say "call endpoint X first" (that is a prerequisite step).
- **Docstrings** — notes describe behavior (e.g. "not thread-safe"); they do not
  say "call this only from the main thread" (that is a constraint in the
  description).
- **Commit bodies** — notes explain why a change was made; they do not give usage
  instructions (those belong in release notes).
- **Error messages** — fix guidance is part of the error text (descriptive +
  imperative), not a separate skipped NOTE.

### Paradigm notes

- **OOP** — notes describe design decisions or state constraints: "NOTE: The
  object enters a disposed state after a call to `dispose()`." (not "you must not
  call other methods").
- **Functional** — notes explain purity/performance: "NOTE: This function is
  pure. It has no side effects." (not "you can memoize it").
- **Procedural (C/Go/Bash)** — notes explain state between steps: "NOTE: The file
  descriptor stays open until the code calls `close()`."
- **Declarative (SQL/Terraform/K8s)** — notes explain platform behavior: "NOTE:
  The `depends_on` attribute controls resource creation order." (not "always set
  this").
- **Systems** — notes clarify compiler-enforced constraints: "NOTE: This function
  borrows the value immutably. The compiler rejects code that violates this
  constraint."

### Grammar notes

- **Descriptive vs imperative mood** — a note uses descriptive mood ("The cache
  expires after 300 seconds."). If a sentence is imperative, it is a work step or
  safety instruction, not a note.
- **Modal verbs in notes** — "can"/"may"/"will" are acceptable when they describe
  system behavior ("The system can process 500 concurrent connections."). "must"
  in a note is a warning sign: move it to a WARNING/CAUTION.
- **Sentence length** — each note sentence ≤ 25 words; split or move to the
  procedure body if longer.
- **Articles** — do not omit articles in notes; the article rule still applies.
- **Technical code nouns** — function/class/command names in notes are technical
  nouns (Rule 1.5); the words around them still must follow approved-vocabulary
  and part-of-speech rules.

### Edge cases

- **Framework names that look like verbs** (React, Express, Spring) — in a note
  they are proper nouns, not imperative verbs: "NOTE: The `React` component tree
  re-renders when the state changes."
- **Generated docs** — fix the source comment, not the generator output; do not
  rely on the generator to filter notes.
- **Interactive tutorials** — "try changing the value" is an instruction;
  acceptable only in exploratory tutorial exercises, never in reference/README/
  API docs.
- **Note that names a command without commanding** — allowed: "NOTE: The
  `terraform plan` command shows the changes Terraform will apply." (descriptive;
  the command name is a technical noun). "Run `terraform plan`" is an instruction
  and not a note.
- **Conditional descriptive clauses** — "if" in a note does not make it an
  instruction if the clause describes system behavior: "NOTE: The server returns
  503 if the upstream does not respond within 10 seconds." (descriptive). "If you
  get a 503, check the health endpoint" is a troubleshooting step, not a note.

## Cross-references (Section 5)

- **Rule 1.1** (Approved Words) — short, approved words make 20-word sentences
  easier; modal verbs in 5.3 often violate 1.1.
- **Rule 1.2** (Part of Speech) — wrong part of speech produces wordy
  constructions that exceed the limit.
- **Rule 1.4** (Approved Verb Forms) — non-standard verb forms add words; the
  base imperative form is the approved form.
- **Rule 1.5** (Technical Code Nouns) — long technical names are allowed;
  abbreviate after first definition to stay within the limit.
- **Rule 1.7** (No Technical Nouns as Verbs) — nominalizations add words
  ("perform an initialization" → "initialize").
- **Rule 1.12** (Technical Verbs) — short technical verbs (build, push, run,
  test, lint) keep sentences short.
- **Rule 5.3 ↔ 5.2** — split per 5.2, then check each sentence against 5.1; each
  split sentence must be imperative (5.3).
- **Rule 5.4 ↔ 5.3** — 5.4 supplies the condition, 5.3 supplies the verb form:
  `[condition] , [imperative verb] [object]`.
- **Rule 5.5 ↔ 5.3/5.4** — notes are descriptive only; a condition that leads to
  a command is a step, not a note.
- **Rule 7.1 / 7.2** (Risk Signal Words / Safety Instructions) — WARNING and
  CAUTION are the only contexts where "must" precedes an imperative; safety
  conditions use the condition-before-command pattern inside the safety block.
- **Rule 9.1** (Descriptive Writing) — notes contain descriptive text; Section 9
  applies fully.
