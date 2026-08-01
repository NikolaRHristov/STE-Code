# Level 5 — Clarity Rules: Sentences & Instructions (Section 5)

This slice contains STE-Code Section 5, adapted for people who use LLMs to
generate code documentation. It covers five rules about how to write procedural
and descriptive sentences in software docs:

- Rule 5.1 — Short Sentences (Maximum 20 Words)
- Rule 5.2 — One Instruction Per Sentence
- Rule 5.3 — Imperative (Command) Form for Instructions
- Rule 5.4 — Descriptive Statement Before the Command
- Rule 5.5 — Notes Give Information Only, Not Instructions

STE-Code voice: plain, code-domain, command-form instructions. Word-count and
voice rules apply to *procedural text* (steps the reader executes). They do not
apply to code blocks, terminal output, string literals, or identifier names.
Inside backticks, a code token counts as one word regardless of length
(`Result<T, E>` = 1 word, `async fn` = 2 words).

## Rule 5.1 — Short Sentences (Maximum 20 Words)

**Core rule:** Every sentence in code-documentation *procedures* must be 20
words or fewer. Split long procedural sentences into shorter ones. Warnings and
cautions about security, data loss, or stability must also obey the 20-word limit.

**Notes** (supplementary, non-procedural text) may use up to 25 words per
sentence. Code blocks, command output, and string literals inside code fences
are excluded from the count.

### Why
Long sentences in install steps, setup checklists, debugging workflows, and API
usage guides are hard to follow when the reader is typing commands or writing
code while reading.

### Split long sentences with these techniques
1. **At coordinating conjunctions.** Replace "and/but/or" with a period. Start
   the next sentence with a transition: "Then," "After that," "Next."
2. **Extract conditions.** Move an "if X, then Y" clause into its own sentence
   that precedes or follows the main instruction.
3. **Separate action from purpose.** Put the instruction in one sentence, the
   reason/result in the next.
4. **Use lists.** Convert an enumerating sentence into bulleted/numbered items.
   List items are fragments, not sentences, but keep them short.

**Allowed (8 words):** Run the tests and check the output.
**Not allowed (28):** Run the full test suite with coverage enabled and check
the report for untested paths that might indicate gaps in the test plan.
**Allowed:** Run the full test suite with coverage enabled. Then, check the
report for untested code paths.

### Counting rules
- A sentence ends at `.`, `?`, or `!`. A comma does not end a sentence.
- Hyphenated compounds count as one word ("command-line" = 1).
- Numbers, symbols, parentheticals each count as one word: "(2)" = 1, "HTTP/2" = 1.
- Code tokens in backticks count as one word each. Generics/type params stay
  opaque: `pub async fn fetch_user(id: UserId) -> Result<User, Error>` is one word.

### Edge cases
- **Long proper nouns** (e.g. "Amazon Web Services Elastic Kubernetes Service"):
  use the shortest accepted form on first use, define an abbreviation, then use
  the abbreviation. The abbreviation counts as one word.
- **Generated docs** (Javadoc, Sphinx, rustdoc, TypeDoc): apply the limit to the
  *source docstrings/comments* the generator reads. Fix the source, not the output.
  If the source is third-party/legacy, apply the 25-word descriptive limit and
  document the exception in a style guide.
- **Legal text** (license headers, disclaimers): not procedural. Put it in a
  separate NOTE or "Legal" section, not inside a procedure.
- **Multi-line code mid-sentence:** the code block is excluded. The introducing
  and following sentences must each obey the limit independently.

### Worked example
```bash
# Non-STE (27 words): Set the environment variable HTTP_TIMEOUT to the value
# 30000 which represents the maximum number of milliseconds that the client
# will wait for a response from the upstream server.
# STE:
export HTTP_TIMEOUT=30000
# This value is the maximum wait time in milliseconds for a response.
```

### Cross-references
Rule 1.1 (approved words), Rule 1.2 (part of speech), Rule 1.4 (verb forms),
Rule 1.5 (technical nouns), Rule 1.7 (no technical-noun-as-verb), Rule 1.9
(short technical nouns), Rule 1.12 (technical verbs), Rule 5.2 (active voice),
Rule 5.3 (imperative), Rule 5.5 (notes), Rule 5.7 (lists), Section 8 (word count).

## Rule 5.2 — One Instruction Per Sentence

**Core rule:** Write exactly one instruction in each sentence. Use numbered or
bulleted lists to show step sequence. There is no limit on the number of steps
in a procedure.

**Exceptions — two instructions in one sentence are allowed only when:**
- both actions occur at the same time and cannot be separated (e.g. "Hold the
  Shift key and click Reload"), or
- a result or measurement follows the action immediately and splitting it would
  break the logical flow (e.g. "Measure the leakage. The leakage must not exceed
  0.5 cc/minute").

### Why
A sentence with multiple instructions lets the reader miss or skip an action,
causing config, deploy, or debug errors.

### Apply across doc types
- **README / quick-start:** each numbered step = one instruction.
- **API docs:** one sentence per endpoint operation, per parameter, per return
  field, per error code.
- **Docstrings:** first line = one-sentence summary. Body: one sentence per
  parameter, return value, raised exception, side effect, precondition.
- **Commit subject:** one imperative sentence describing one change. Multiple
  unrelated changes → split the commit (or use body bullets).
- **Error messages:** state exactly one problem; one recovery instruction if
  applicable. Do not combine failure paths with "or/and/also".

**Non-STE (5 instructions):** Open the config file and locate the database
section and change the connection string to staging and save the file and close
the editor.
**STE:** (1) Open `config/database.toml`. (2) Find the `[database]` section.
(3) Set `connection_string = "postgres://staging-db:5432/app"`. (4) Save the
file. (5) Close the editor.

### Grammar (single predicate)
Each imperative sentence has exactly one main verb in imperative mood.
- Correct: `Install the package.` (one predicate)
- Incorrect: `Install the package and configure the settings.` (two predicates)

**Compound objects are fine** (one verb, many objects):
`Remove the log files, cache files, and temporary directories.` — one instruction.
`Remove the log files and restart the server.` — two instructions (split).

**"-ing" forms as main verbs hide instructions:** "After installing, configuring,
and setting up, run the app" smuggles three instructions. Number them.

**Preconditions are instructions:** "Before you run the tests, set TEST_MODE" →
`(1) Set TEST_MODE to true. (2) Run the tests.`

### Edge cases
- **Framework CLI commands** (`docker compose up`, `kubectl apply`,
  `terraform destroy`) are one technical noun phrase. Do not split into
  "run docker. then compose." Use backticks.
- **Error messages with cascading symptoms:** state the *root cause* (one
  sentence); list consequences in a separate descriptive sentence.
- **Generated docs:** prefer annotation styles (JSDoc `@param` per item) that
  yield one sentence per item.
- **Test assertions:** one description/message per assertion.
- **Progress logs:** each log line reports one completed action/result.

### Cross-references
Rule 5.1 (short sentences), Rule 5.3 (imperative), Rule 1.1 (approved words),
Rule 1.12 (technical verbs), Rule 1.13 (no technical-verb-as-noun), Rule 5.5
(notes), STE-Code Dictionary (approved action verbs).

## Rule 5.3 — Imperative (Command) Form for Instructions

**Core rule:** Write every procedural instruction in the imperative (command)
form. Start each instruction with an imperative verb. The implied subject is
always the reader ("you"), which removes ambiguity about who acts.

**Imperative verbs common in code docs:** run, set, open, save, install,
configure, restart, execute, copy, delete, create, add, enter, select, click,
type, check, use, start, stop, send, show, get, make, remove, build.

**Do NOT use:**
- passive voice ("is executed", "are to be removed"),
- gerunds as commands ("Building the image..."),
- modal verbs (can, could, should, may, might) for instructions,
- "must" before the imperative in a *standard* instruction.

**Reserve "must"** for WARNING/CAUTION blocks about security, data loss, or
safety-critical conditions.

### What kind of text is imperative vs descriptive?
| Text type | Form |
|-----------|------|
| Install/setup/quick-start steps | Imperative |
| API "getting started"/auth walkthrough | Imperative |
| Endpoint *descriptions* (system behavior) | Descriptive ("Returns a list") |
| Docstring body (what code does) | Descriptive |
| Commit **subject line** | Imperative ("Fix the race condition") |
| Commit body (rationale) | Descriptive allowed |
| Error message — recovery instruction | Imperative (after the description) |
| Makefile/shell-script usage headers | Imperative |

### Examples
- Non-STE: The unit tests can be executed with `npm test`.
  STE: Run the unit tests with `npm test`.
- Non-STE: The configuration file should be validated before the app starts.
  STE: Check the configuration file against the schema before you start the app.
- Non-STE: It is recommended that you create a backup before the migration.
  STE: Create a backup of the database before you run the migration.
- Non-STE: The SSL certificate must be renewed and then the server must restart.
  STE: Renew the SSL certificate. Then, restart the web server to apply changes.
- WARNING (allowed "must"): IF YOU MUST STORE CREDENTIALS, ALWAYS USE AN
  ENCRYPTED SECRETS MANAGER. PLAIN-TEXT CREDENTIALS CAN CAUSE BREACHES.

### Grammar
- **Subject omission:** imperative drops "you" → reader knows the instruction is
  for them. Passive hides the agent ("The file is saved" = who?).
- **Modal elimination:** "can/should" let the reader read an action as optional.
  Imperative leaves no room for that.
- **Tense consistency:** base verb form, no inflection — simpler to translate and
  parse.
- **Coordinates with Rule 5.4:** a descriptive context sentence may precede the
  imperative command. Keep the two roles in separate sentences.
  `The Docker daemon must be running. Build the image with \`docker build\`.`

### Paradigm notes
- **OOP:** imperative for setup/config; descriptive for invariants/inheritance.
- **Functional:** imperative for build/REPL/setup; descriptive for what a
  function transforms.
- **Procedural (C/Go/Bash):** imperative dominates (build, compile, link, run).
- **Declarative (SQL/Terraform/K8s):** the spec is descriptive; the *tooling
  that applies it* (CLI, pipelines) is imperative.
- **Systems (Rust/C):** descriptive for invariants; imperative for "how to
  comply" (free memory, satisfy borrow checker).

### Edge cases
- **Framework name = verb** (React, Spring, Go, Make, Build): never start a
  sentence with the framework name as if it were a command. Prefix with an
  article or reword: "Use React to build the UI." Avoid "React to state changes."
- **Generated/tool output** (`--help`, changelogs, OpenAPI pages): fix the
  *template/source*, not the output. CLI help: `help="Write the output to this file"`.
- **Language keywords that are modals** (`try`, `await`, `yield`): use backticks;
  don't start an imperative sentence with the bare keyword. "Use `await` on the
  promise before you access the result."
- **Release notes:** imperative for upgrade/migration steps; past/perfect tense
  for feature/bug descriptions.
- **Interactive tutorials:** label instructional blocks ("Run this command") and
  system-response blocks ("You will see…") separately.

### Cross-references
Rule 1.1 (approved words), Rule 1.2 (part of speech), Rule 1.4 (verb forms),
Rule 1.7 (no technical-noun-as-verb), Rule 5.4 (descriptive before command),
Rule 7.1 (risk signal words), Rule 7.2 (safety instruction start), STE-Code
Dictionary (approved verbs: use > utilize, start > initiate, check > verify,
set > configure).

## Rule 5.4 — Descriptive Statement Before the Command

**Core rule:** When a step has a condition the reader must know first, write the
condition as a descriptive statement at the start of the sentence, follow it with
a **comma**, then give the imperative command. The comma is mandatory — it marks
where the condition ends and the instruction begins.

**Pattern:** `[condition clause] , [imperative verb] [object]`

- Non-STE: Run the migration after you set `DATABASE_URL` and confirmed the
  server accepts connections.
- STE: After you set the `DATABASE_URL` environment variable, run the migration
  script.

### Why the comma matters
Comma placement changes which verb an adverb modifies:
- `If the service does not start, automatically restart it.` (the restart is automatic)
- `If the service does not start automatically, restart it.` (you restart it manually)

In code, condition clauses often contain punctuation (backticks, dots,
parentheses). The comma after the clause is the only reliable boundary marker.

### Apply across doc types
- **README:** one condition-command pair per step. Don't bury the condition after
  the command.
- **API:** state the trigger/error condition before describing the response.
- **Docstrings:** precondition-before-behavior. "If the file does not exist, this
  function raises `FileNotFoundError`."
- **Commit:** context-before-action. "When the connection pool reaches capacity,
  add a mutex lock around pool access."
- **Error messages:** problem-before-resolution. "The config has invalid YAML on
  line 42. Fix the syntax error, then run the app again."

### Dependent clause types (condition first, comma, command)
1. **Time** (before, after, when, while, until): `Before you deploy, run the tests.`
2. **Conditional** (if, unless): `If the build fails, check the error log.`
3. **Reason** (because): prefer splitting — "The port is in use. Use a different port."
4. **Purpose** (to, in order to): `To see running containers, run \`docker ps\`.`
5. **Concessive** (although): `Although the server starts, check the health endpoint.`

Never reverse the order (command first, condition second) — the reader would act
before learning the condition.

### Multiple conditions in one step
- **A — separate sentences:** "Make sure the server is running. After it accepts
  connections, run the migration."
- **B — compound with 'and':** "If the server is running and the backup is
  complete, run the migration."
- **C — sequential pairs (preferred):** "Before you run the migration, make sure
  the server is running. After the server accepts connections, run the migration."

### Paradigm notes
- **OOP:** state preconditions before method-call/constructor instructions.
- **Functional:** state input guard/pattern before describing the transformation.
- **Procedural (C/Go/Bash):** state system-state condition before the action.
- **Declarative:** applies to the *operational wrapper* (how to apply/destroy),
  not the declarative spec itself.
- **Systems (Rust/C):** state safety condition before the operation; use WARNING/
  BREAKING when the consequence is severe.

### Edge cases
- **Framework name = common word** (Next.js, Express): still a technical noun;
  comma rule applies to the condition clause containing it.
- **Code keyword inside condition:** comma after the closing backtick. "When
  `response.status === 429`, wait for the `Retry-After` duration. Then, retry."
- **Condition clause has its own commas** (a list): restructure into a separate
  descriptive sentence + a simple condition clause, or use Strategy C. Don't pile
  commas.
- **Condition implied by tool output:** state the observable output as the
  condition. "If the terminal shows 'Connection refused', start the database."
- **Generated docs:** relaxed for output, but source docstrings/comments must
  follow the rule. For templates, place the condition placeholder first.

### Cross-references
Rule 1.1 (approved words), Rule 1.4 (verb forms), Rule 1.5 (technical nouns),
Rule 5.3 (imperative verb form), Rule 5.5 (notes), Rule 7.2 (safety instruction
start). Dictionary synonyms: verify → check, obtain → get, terminate → stop.

## Rule 5.5 — Notes Give Information Only, Not Instructions

**Core rule:** A NOTE gives descriptive information only. It must not contain
instructions, commands, step-by-step actions, requirements, limits, tolerances,
or expected results of a work step. A note must not use the imperative form.

Each sentence in a note may be up to 25 words. A note can have one or more
sentences.

### The "remove the notes" test
To check correct note usage: read the procedure *without* the notes. If the
reader can complete the procedure correctly, the notes are used correctly. If
important information is only in a note, move it into a numbered work step and
repeat the test.

### Move note content out when…
- it tells the reader to run a command → make it a numbered work step.
- it states a limit/tolerance/result → put it directly in the work step after the
  related action.
- it carries safety-critical info (data loss, security, system damage) → convert
  to a WARNING or CAUTION safety instruction. A note is never a substitute for a
  safety instruction.

**Non-STE:** NOTE: When you update dependencies, run `npm audit fix` to resolve
vulnerabilities. If you skip this, you may have security issues.
**STE:** (5) Run the command `npm audit fix` to resolve known vulnerabilities.

**Non-STE:** NOTE: Do not run the migration on production without a backup.
**STE:** WARNING: DO NOT RUN THE MIGRATION ON THE PRODUCTION DATABASE WITHOUT A
FULL BACKUP. RUNNING IT WITHOUT A BACKUP CAN CAUSE IRREVERSIBLE DATA LOSS.

### Apply across doc types
- **README:** notes give project context (why a dependency exists). Not install steps.
- **API docs:** notes explain behavior/side effects/constraints. "Call the
  /refresh endpoint first" is an instruction — move it to the endpoint description.
- **Docstrings:** describe behavior/constraints. "Call `initialize()` first" is a
  requirement — write it as a descriptive constraint in the function spec.
- **Commit body:** explain *why* a change was made. Not "run the migration" (that
  belongs in release notes / upgrade guide).
- **Error messages:** the fix guidance is part of the error text (descriptive +
  imperative), not a separate note the reader might skip.

### Paradigm notes
- **OOP:** note explains disposed-state constraint, not "call dispose() first."
- **Functional:** note states purity/performance, not "memoize it."
- **Procedural:** note states resource-leak behavior, not "close the fd."
- **Declarative:** note describes attribute behavior, not "always set this."
- **Systems:** note describes borrow/compiler behavior, not "don't mutate."

### Grammar of notes
- **Descriptive mood only.** Subject performs/experiences the action (system,
  code, environment). "The cache expires after 300 seconds." NOT "Run the build."
- **Modals:** "can/may/will" are fine when describing system behavior. "must" in
  a note is a red flag — it usually signals a requirement that belongs in a work
  step or WARNING.
- **Articles:** do not omit "the/a/an" in notes.
- **Technical nouns** (function/class/command names) follow Rule 1.5 — exempt from
  the dictionary, but surrounding words must use approved vocabulary.

### Edge cases
- **Framework name = verb** (React, Express): still a technical noun in a note;
  not an instruction. "The `React` component tree re-renders when state changes."
- **Generated docs:** fix the *source comment*, not the generator output.
- **Interactive tutorials:** exploratory "try this" notes are acceptable only in
  non-shipping tutorial material, never in reference/README/API docs.
- **Command referenced, not commanded:** "The `terraform plan` command shows the
  changes" is a note. "Run `terraform plan`" is an instruction — not a note.
- **Conditional in a note:** "if" alone doesn't make it an instruction. Test: does
  the clause describe system behavior (note) or tell the reader to do something
  (a step)? "The server returns 503 if upstream is slow" = note. "If you get 503,
  check /health" = step.

### Cross-references
Rule 1.1 (approved words), Rule 1.5 (technical nouns), Rule 1.7 (no
technical-noun-as-verb), Rule 5.3 (imperative vs descriptive), Rule 5.4
(descriptive-before-command — a note must not follow this pattern), Rule 5.6
(separate steps for separate actions), Rule 7.1 (risk signal words), Rule 9.1
(descriptive writing).

## Quick checklist for LLM code-doc generation

When generating install steps, API guides, READMEs, docstrings, commit messages,
or error text, apply Section 5 in this order:

1. **5.3 — Use imperative verbs** for every instruction. Drop passive voice,
   gerunds, and modals (can/should/may). Reserve "must" for WARNING/CAUTION.
2. **5.2 — One instruction per sentence.** Number steps. Split compound
   instructions. Don't put preconditions, results, or "and"-chained actions in one
   sentence unless they are simultaneous or an immediate result.
3. **5.1 — Keep each procedural sentence ≤ 20 words** (notes ≤ 25). Exclude code
   blocks and count backtick tokens as one word each. Split long sentences at
   conjunctions/conditions or into lists.
4. **5.4 — Put the condition before the command**, with a comma.
   `After you set DATABASE_URL, run the migration.` Never reverse the order.
5. **5.5 — Keep NOTES descriptive only.** No imperatives, no commands, no limits.
   If a note tells the reader to act, make it a work step (or a WARNING). A note
   sentence may be up to 25 words.

Defaults that are NOT instructions: code blocks, terminal output, string literals,
identifier names, and the words around a backticked technical noun.
