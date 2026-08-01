# Level 4 — Grammar: Sentence Construction and Technical Noun Phrasing

Rules 2.1–2.3 of STE-Code govern how you build sentences in code
documentation: how to write technical nouns, how long a noun phrase may be,
and how to hyphenate compound modifiers. This slice is the "grammar" layer —
it sits on top of the word rules (Section 1) and below the sentence-type
rules (Section 3+).

When you generate or review code documentation with an LLM, apply these three
rules before any sentence leaves your hands:

1. Keep every technical noun phrase to **three words or fewer** (Rule 2.1).
2. When a noun must be longer, **write it in full on first use**, then use a
   short form or approved abbreviation (Rule 2.2).
3. **Hyphenate only related words used as one unit**, never a chain of more
   than three words (Rule 2.3).

These rules exist because a reader scans docs fast. A stacked noun such as
`authentication_token_expiration_refresh_interval_setting` hides which part
owns which. The fix is plain English structure: short nouns joined by
prepositions.

---

## Rule 2.1 — Keep technical nouns short

To keep multi-word technical nouns short, use prepositions (for example "of,"
"on," "in," and "for") and explain the multi-word technical nouns. Write each
multi-word technical noun as a short noun that uses prepositions to make the
meaning clear.

A technical noun that the code domain uses — a module name, a class name, a
configuration key, an endpoint path, an error type, or a test fixture — must
stay short so the reader can parse it without effort.

### Why this matters in code documentation

- A reader scans docs fast. A stacked noun hides the ownership tree: the
  setting belongs to the interval, the interval belongs to the expiration,
  the expiration belongs to the token.
- Short technical nouns match how code is already structured. A config key, a
  class, or a JSON field is one short concept. Prepositions in the sentence
  show how those short concepts relate.
- Follow the Microsoft and Google style guides: use short, plain words. Do not
  use `utilize`, `leverage`, or `employ` when `use` is enough. Do not use
  `commence`, `initiate`, or `terminate` when `start` and `stop` are enough.
  Keep the verb simple and the noun short.
- Approved code-domain adjectives stay attached to the short noun they modify:
  `idempotent`, `immutable`, `thread-safe`, `atomic`, `nullable`,
  `deprecated`, `stateless`, `backward-compatible`, `asynchronous`,
  `concurrent`, `deterministic`. Write `the idempotent retry policy`, not
  `idempotentretrypolicy`.

### How to apply the rule

1. Find a noun that stacks two or more modifiers (a "noun chain").
2. Split the chain at the ownership or containment points.
3. Connect the parts with `of`, `on`, `in`, or `for`.
4. If a part is itself a code component, name it with its short technical noun
   (its class, key, or file), not a merged word.
5. In instruction text, use the approved verbs: `set`, `get`, `make`, `show`,
   `check`, `remove`, `send`, `start`, `stop`, `use`, `update`. Do not use
   `configure` for `set`, `retrieve` for `get`, `delete`/`purge` for
   `remove`, or `display` for `show`.

### Examples in STE-Code

| Non-STE (stacked noun) | STE (short nouns + prepositions) |
|---|---|
| Authentication token expiration refresh interval setting | Setting of the refresh interval of the expiration of the authentication token |
| Install the forward service request validator middleware config tags. | Install the config tags on the validator middleware of the request of the forward service. |
| Remove the database migration script output directory lock files. | Remove the lock files that lock the output directory of the migration script of the database. |
| Adjust to obtain cache invalidation hook alignment with the event emitter. | Adjust the cache invalidation hook until it aligns with the event emitter. |
| Payment gateway timeout retry exhaustion notification handler. | Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway. |
| User account profile avatar image storage bucket policy update. | Update of the policy of the storage bucket of the image of the avatar of the profile of the user account. |
| The inbound request rate limit window reset schedule controls the burst. | The schedule of the reset of the window of the rate limit of the inbound request controls the burst. |
| The background worker queue overflow alert suppression rule runs on the staging cluster. | The alert suppression rule on the overflow of the background worker queue runs on the staging cluster. |

```yaml
# STE-Code: short keys, one concept per level
auth:
  token:
    expiration:
      refresh_interval_seconds: 300   # setting of the refresh interval of the expiration of the authentication token

# Non-STE: one long key hides the relationship (do not write this)
authentication_token_expiration_refresh_interval_setting: 300
```

```python
# STE-Code doc comment
def get_refresh_interval(token):
    """Return the setting of the refresh interval of the expiration of the authentication token."""
    return token.expiration.refresh_interval_seconds
```

> **See also:** Rule 1.5 (what counts as a technical noun), Rule 1.3 (keep
> verbs and nouns plain: use, set, get, remove, check, update, show), Rule 2.2
> (write long technical nouns in full), Rule 2.3 (hyphenate related words).

---

## Rule 2.2 — Write long technical nouns in full

When a technical code noun has more than three words, write it in full. Then
use one of these methods to make the technical code noun clear:

- Give a shorter form of the technical code noun.
- Use hyphens (-) between words that you use as one unit.
- Use prepositions (for example "of," "on," "in," "for," and "to") to split a
  long noun into short, separate parts (see Rule 2.1).

A long multi-word code noun can be a long technical noun, or it can be a
combination of shorter technical nouns. Frequently, it is not possible to divide
technical code nouns into smaller parts because they are the technical nouns
that your company, framework, or subject field uses. Thus, you must write
technical code nouns as they are, in their approved form.

### Method 1 — Shorter form of technical code nouns

If a long technical code noun comes from an official code document (for
example, an API specification, a schema, an OpenAPI file, or an architecture
diagram), write it in full the first time that it occurs in the text. Then, if
it is possible, explain the technical code noun and in the remaining text of
your document, use a shorter form or an approved abbreviation.

Before you do this procedure, initialize the user session cache invalidation
lock handler (the handler that locks the cache of the user session, referred to
in this procedure as the "invalidation lock handler").

In this example, you write "user session cache invalidation lock handler" in
full. Then, after an explanation, you give a shorter technical code noun:
"invalidation lock handler." This shorter technical code noun has three words
and obeys rule 2.1.

```python
# STE-Code: write the long technical code noun in full, then use the short form
def initialize_session_lock(user_id: str) -> None:
    """Initialize the user session cache invalidation lock handler.

    The invalidation lock handler locks the cache of the user session so that
    a background job cannot read stale data while a write is in flight.
    """
    handler = UserSessionCacheInvalidationLockHandler(user_id)
    handler.engage()   # from here, refer to it as the "invalidation lock handler"
```

The Main Form Validation Module (MFVM) is a TypeScript module that includes a
Main Export Controller Unit (MECU) and a Data Bridge (DB). The MFVM is installed
in the application core layer and operates in the form submission system. The
function of the MFVM is to validate and submit the form data from the Main Form
Provider (MFP) to the data stores and the validation hooks. The Dynamic Config
Unit (DECU) sends events to operate the MFVM.

In this example, the explanation is not necessary because the text gives all the
necessary information about the module. You write all official technical code
nouns that include more than three nouns in full the first time that they
occur. Then, in the remaining parts of the text, you use their related approved
abbreviations.

```typescript
// STE-Code: abbreviation defined on first use, then reused
// The Main Form Validation Module (MFVM) is a TypeScript module that
// includes a Main Export Controller Unit (MECU) and a Data Bridge (DB).
interface FormPayload { fields: Record<string, unknown>; }

class MainFormValidationModule {       // MFVM
  constructor(
    private readonly exportController: MainExportControllerUnit,  // MECU
    private readonly bridge: DataBridge,                          // DB
    private readonly config: DynamicConfigUnit,                  // DECU
  ) {}

  submit(payload: FormPayload): void {
    this.config.onEvent("submit", () => this.exportController.run(payload));
  }
}
```

If an approved technical code noun includes three words or less, it is not
necessary to use abbreviations.

You can use abbreviations that come from your official code documentation but
be careful. A text full of abbreviations in a procedure, although shorter, is
not easy to read.

```yaml
# STE-Code: name each part in full; do not pack the parts into letter codes
controller:
  data_transformer_assembly:   # (8)  part of the view body
  pipeline_validator_assembly: # (15) sits on its seat
  buffer_assembly:             # (17) part of the view body

# Non-STE (do not write this):
#   parts: [DTA_8, PVA_15, BA_17, VB_20]
```

### Method 2 — Use prepositions to break up a long noun

When a long technical code noun is a chain of short nouns (for example "user
authentication token refresh failure retry policy"), it is hard to read and
easy to parse the wrong way. Make the main noun the head of the sentence, then
add the rest with prepositions. Put the key noun first, then attach the
modifiers with "of," "on," "in," "for," or "to." This keeps each part short
while the full idea stays clear.

| Non-STE | STE |
|---|---|
| Configure the user authentication token refresh failure retry policy before you deploy the service to production. | Configure the retry policy for the failure of the refresh of the user authentication token before you deploy the service to production. |
| Install the background worker queue overflow alert suppression rule on the staging cluster. | Install the alert suppression rule on the overflow of the background worker queue on the staging cluster. |
| Remove the database connection pool exhaustion recovery timeout configuration parameter from the settings file. | Remove the configuration parameter that sets the recovery timeout for the exhaustion of the database connection pool from the settings file. |
| Update the build script to obtain output directory naming consistency with the package convention. | Update the build script until the output directory naming is consistent with the package convention. |

```python
# STE-Code: the short noun keeps the function name and the docstring clear
def set_recovery_timeout(pool, seconds: float) -> None:
    """Set the configuration parameter that sets the recovery timeout
    for the exhaustion of the database connection pool."""
    pool.config["recovery_timeout_seconds"] = seconds
```

### Method 3 — Hyphenate words that you use as one unit

When two or more words act as a single modifier before a noun, use a hyphen (-)
to show that they are one unit. This stops the reader from grouping the words
the wrong way. In code prose, hyphenate compound modifiers such as
"request-response," "read-write," "build-time," "out-of-band," "end-to-end,"
and "run-time." Do not hyphenate the modifier when the first word is an adverb
that ends in "-ly" (for example "a publicly documented API" stays open).

| Non-STE | STE |
|---|---|
| Set the request response mapping handler to the new schema before the migration. | Set the request-response mapping handler to the new schema before the migration. |
| Run the build time configuration check after you compile the module. | Run the build-time configuration check after you compile the module. |
| Add an end to end test for the payment flow before you merge the change. | Add an end-to-end test for the payment flow before you merge the change. |
| Use the out of band signal to stop the long running job. | Use the out-of-band signal to stop the long-running job. |

```python
# STE-Code: hyphenated modifiers are one unit in code identifiers too
def handle_request_response(handler: "RequestResponseMappingHandler") -> None:
    """Set the request-response mapping handler to the new schema."""
    handler.apply(schema=SCHEMA_V2)

def run_build_time_check() -> None:
    """Run the build-time configuration check after you compile the module."""
    ...
```

Note: Hyphenation groups words into one unit but does not make a long technical
noun short. If the hyphenated unit still has more than three words (for example
"request-response mapping handler"), write it in full the first time, then use
the shorter form ("mapping handler") in the rest of the text.

### How to apply the rule in code documentation

1. Find the long technical code noun (more than three words) in your sentence.
2. Write it in full the first time it occurs. If it comes from an official
   source (API spec, schema, architecture diagram), keep the exact approved
   form.
3. Give a shorter form or an approved abbreviation right after the full form, in
   parentheses.
4. In the rest of the document, use only the shorter form or the approved
   abbreviation.
5. If the noun is a chain of short nouns, split it with prepositions so each
   part is short (see Rule 2.1).
6. If two or more words act as one modifier, hyphenate them.
7. Do not fill a procedure with abbreviations. A short, clear noun is better
   than a string of letters.

> **Microsoft / Google style note:** Use short, plain words. Do not use
> `utilize`, `leverage`, or `employ` when `use` is enough. Do not use
> `commence`, `initiate`, or `terminate` when `start` and `stop` are enough.
> Keep the verb simple and the noun short.

> **See also:** Rule 2.1 (keep technical nouns to three words or fewer), Rule
> 1.5 (technical noun categories), Rule 1.3 (use approved words: use, set, get,
> make, show, check, remove, send, start, stop).

---

## Rule 2.3 — Use hyphens between words used as one unit

A hyphen is a punctuation mark that connects words or parts of words. Use
hyphens between words to show how related words operate as one unit. This
method will make the multi-word code nouns that you use agree with rule 2.1.
Hyphenated words always count as one word, so a hyphenated code noun fills only
one of the three-word slots that rule 2.1 allows for a noun phrase.

Do not connect words that are not related, because the hyphen will change the
meaning of the multi-word code noun. If you are not sure, only explain the
multi-word code noun in the clearest way. Then, use a shorter form, an approved
verb such as `get`, `set`, `make`, `start`, or an official approved
abbreviation from your glossary.

If an approved technical code noun includes hyphens — for example
`input-output stream`, `thread-safe queue`, or `backward-compatible API` — do
not change it. If it is too long, write it in full the first time it occurs and
then use the recommended method for shorter technical nouns that this rule
specifies.

Do not use hyphens to make groups of more than three words. If you hyphenate
all the words, this multi-word code noun will not be easy to read and
understand. Keep the hyphen group to at most three words; split longer chains
with prepositions such as `of`, `on`, or `in`.

### Examples in STE-Code

| Example | Note |
|---|---|
| Make sure that the fail-safe shutdown-handler connection is safe. | (3 words: make / sure / connection) |
| Inspection of the request rate-limit device. | (3 words: inspection / of / device) |
| The thread-safe queue keeps the order of the write operations. | (3 words: queue / keeps / order) |
| Remove the backward-compatible API client before you make the change. | (3 words) |

When a hyphen joins two related words, the pair counts as one unit. Apply this
in procedural and descriptive code documentation so that the reader can parse
the noun without re-reading it.

#### Full example — hyphenate related words, keep to three words

A README step that names a combined component must keep the three-word limit of
rule 2.1. Hyphenate only the related pair; do not chain every word.

> **Non-STE:** Move the `main-feature-flag-rollback-handler` trigger to start
> the test run. (2 words, but not correct — four words joined as one unit)
>
> **STE:** Move the `main-feature-flag` rollback-handler trigger to start the
> test run. (3 words: move / trigger / run)

```bash
# STE-Code compliant: the hyphen joins the related pair only
make test trigger=rollback-handler flag=main-feature-flag
```

```python
# STE: the multi-word noun is "main-feature-flag" (1 unit) + "rollback-handler"
# (1 unit) + "trigger" (1 unit)
def move_trigger(main_feature_flag: str, rollback_handler: str) -> None:
    """Move the main-feature-flag rollback-handler trigger to start the test run."""
    trigger = f"{main_feature_flag}:{rollback_handler}"
    start_test_run(trigger)
```

#### Full example — do not hyphenate a three-word approved technical noun

When the official name of a component is three words or less, leave the spaces.
Hyphenating it changes the count and can confuse the reader.

> **Non-STE:** A. Remove the `data-adapter` assembly (8) from the view body
> (20). B. Remove the `pipeline-validator` assembly (15) from its seat.
>
> **STE:** A. Remove the `data adapter` assembly (8) from the view body (20).
> B. Remove the `pipeline validator` assembly (15) from its seat.

```python
# STE: "data adapter" and "pipeline validator" are each a 2-word technical
# noun, not hyphenated
def remove_assembly(name: str, part_id: int) -> None:
    """Remove the data adapter assembly (part_id) from the view body."""
    detach(name, part_id)
    log(f"removed {name} assembly {part_id}")

remove_assembly("data adapter", 8)
remove_assembly("pipeline validator", 15)
```

#### Full example — keep a hyphen that the official name already has

If your official code documentation or an approved standard already hyphenates
a technical noun, keep the hyphen. Removing it changes the term.

> **Non-STE:** Do not write: The `input output stream` is part of the logging
> system.
>
> **STE:** WRITE: The `input-output stream` is part of the logging system.

```python
# STE: "input-output stream" keeps its hyphen because the standard defines it
# that way
class LoggingSystem:
    def __init__(self, stream: "InputOutputStream") -> None:
        # The input-output stream is part of the logging system.
        self.stream = stream

    def write(self, message: str) -> None:
        self.stream.push(message)
```

```yaml
# STE-Code config excerpt
logging:
  # The input-output stream is part of the logging system.
  input-output-stream:
    buffer-size: 4096
    flush-on-error: true
```

> **See also:** Rule 2.1 (write nouns as nouns and keep noun phrases to three
> words), Rule 1.5 (where hyphenated code terms such as `thread-safe queue` and
> `backward-compatible API` are defined), Rule 2.2 (use approved verbs and keep
> sentences short).

---

## Quick reference for LLMs

When you write or review code documentation, enforce these grammar checks in
order:

1. **Noun length** — Every technical noun phrase has at most three words.
   Split longer chains with prepositions (`of`, `on`, `in`, `for`, `to`).
2. **Long nouns** — A noun longer than three words is written in full on first
   use, then referred to by a short form or approved abbreviation defined in
   parentheses on first use.
3. **Hyphens** — Hyphenate only a related pair or triple used as one modifier
   before a noun (`request-response`, `build-time`, `end-to-end`). Never
   hyphenate a chain of more than three words; never hyphenate a 3-word
   approved technical noun (`data adapter`, not `data-adapter`).
4. **Verbs** — Pair technical nouns with short approved verbs: `set`, `get`,
   `make`, `show`, `check`, `remove`, `send`, `start`, `stop`, `use`,
   `update`. Avoid inflated verbs (`utilize`, `leverage`, `commence`,
   `initiate`, `terminate`).
5. **Abbreviations** — An abbreviation is allowed only when it is defined in
   official documentation on first use and reused consistently. Do not fill a
   procedure with abbreviation strings.

These three rules (2.1–2.3) plus the word rules (1.1–1.14) are the grammar
core of STE-Code for code documentation.
