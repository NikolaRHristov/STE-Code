# Level 4 — Section 2: Noun Phrases

Section 2 of STE-Code controls how you write technical nouns in code
documentation: API docs, README sections, commit messages, runbooks, code
comments, config files, and test names.

Three rules, one idea: **a technical noun must be short enough to parse on the
first read.**

| Rule | Statement | Primary tool |
|---|---|---|
| 2.1 | Keep technical nouns short. | Prepositions (`of`, `on`, `in`, `for`) |
| 2.2 | When a technical noun has more than three words, write it in full. | Short form or approved abbreviation on first use |
| 2.3 | Use hyphens between words used as one unit. | Hyphen, max three words per group |

Shared constraints across all three rules:

- Maximum three words in a noun phrase. A hyphenated unit counts as one word.
- Approved verbs only: `set`, `get`, `make`, `show`, `check`, `remove`, `send`,
  `start`, `stop`, `use`, `update`.
- Forbidden substitutions: `configure`→`set`, `retrieve`→`get`,
  `delete`/`purge`→`remove`, `display`→`show`, `utilize`/`leverage`/`employ`→`use`,
  `commence`/`initiate`→`start`, `terminate`→`stop`.
- Approved code-domain adjectives stay attached to the noun they modify:
  `idempotent`, `immutable`, `thread-safe`, `atomic`, `nullable`, `deprecated`,
  `stateless`, `backward-compatible`, `asynchronous`, `concurrent`,
  `deterministic`.

---

## Rule 2.1 — Keep Technical Nouns Short

> Source: ASD-STE100 Issue 9, Rule 2.1 · Group `005-rules-sec-2` · spec pages 60–63.

**Rule.** To keep multi-word technical nouns short, use prepositions (`of`,
`on`, `in`, `for`) and explain the multi-word technical noun. A technical noun
that the code domain uses — a module name, a class name, a configuration key,
an endpoint path, an error type, a test fixture — must stay short so that the
reader can parse it without effort.

When a phrase names a code component with more than a few words, break the
phrase into small nouns joined by prepositions. Do not stack modifiers into one
long noun.

**Why it matters.**

- A stacked noun such as `authentication_token_expiration_refresh_interval_setting`
  hides which part owns which. Prepositions show the tree: the setting belongs
  to the interval, the interval to the expiration, the expiration to the token.
- Short technical nouns match how code is already structured. A config key, a
  class, or a JSON field is one short concept; prepositions show how those
  concepts relate.
- Long merged identifiers are hard to grep and hard to read in a log line.

**Procedure.**

1. Find a noun that stacks two or more modifiers (a "noun chain").
2. Split the chain at the ownership or containment points.
3. Connect the parts with `of`, `on`, `in`, or `for`.
4. If a part is itself a code component, name it with its short technical noun
   (its class, key, or file), not a merged word.
5. In instruction text, use the approved verbs.

### Rewrite pairs

| Context | Non-STE (do not write) | STE-Code |
|---|---|---|
| Config key | Authentication token expiration refresh interval setting | Setting of the refresh interval of the expiration of the authentication token |
| Deployment labels | Install the forward service request validator middleware config tags. | Install the config tags on the validator middleware of the request of the forward service. |
| Cleanup task | Remove the database migration script output directory lock files. | Remove the lock files that lock the output directory of the migration script of the database. |
| Test setup | Adjust to obtain cache invalidation hook alignment with the event emitter. | Adjust the cache invalidation hook until it aligns with the event emitter. |
| API doc | Payment gateway timeout retry exhaustion notification handler. | Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway. |
| Commit title | User account profile avatar image storage bucket policy update. | Update the policy of the storage bucket of the image of the avatar of the profile of the user account. |
| README | The inbound request rate limit window reset schedule controls the burst. | The schedule of the reset of the window of the rate limit of the inbound request controls the burst. |
| Code comment | The background worker queue overflow alert suppression rule runs on the staging cluster. | The alert suppression rule on the overflow of the background worker queue runs on the staging cluster. |

### Worked examples

Configuration key — one concept per level, relationship stated with `of`:

```yaml
# STE-Code
auth:
  token:
    expiration:
      refresh_interval_seconds: 300   # setting of the refresh interval of the
                                      # expiration of the authentication token

# Non-STE: one long key hides the relationship (do not write this)
authentication_token_expiration_refresh_interval_setting: 300
```

```python
# STE-Code doc comment
def get_refresh_interval(token):
    """Return the setting of the refresh interval of the expiration of the
    authentication token."""
    return token.expiration.refresh_interval_seconds
```

Deployment labels — name the target with prepositions so the reader knows what
the tag goes on:

```bash
# STE-Code: the tag goes on the validator middleware of the request
#           of the forward service
kubectl label pods \
  -l app=forward-service \
  middleware=validator \
  config=enabled
```

Cleanup task — approved verb `remove` (not `delete`, not `purge`):

```python
# STE-Code: remove the lock files that lock the output directory
#           of the migration script of the database
from pathlib import Path

def remove_migration_lock_files(db_name: str) -> int:
    """Remove the lock files that lock the output directory of the
    migration script of the database."""
    output_dir = Path("migrations") / db_name / "output"
    removed = 0
    for lock in output_dir.glob("*.lock"):
        lock.unlink()
        removed += 1
    return removed


# Test that checks the cleanup (use `check`, not `verify`)
def test_remove_migration_lock_files(tmp_path):
    out = tmp_path / "app" / "output"
    out.mkdir(parents=True)
    (out / "write.lock").write_text("")
    assert remove_migration_lock_files("app") == 1
    assert not any(out.glob("*.lock"))
```

Test setup — name the hook, then state what it aligns with:

```python
# STE-Code: adjust the cache invalidation hook until it aligns with the
#           event emitter
import time

def align_cache_hook(hook, emitter, timeout: float = 5.0) -> bool:
    """Adjust the cache invalidation hook until it aligns with the event emitter."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if hook.target is emitter:
            return True
        hook.nudge()
    return False
```

API doc and log lines — split so each level is a short noun:

```python
# STE-Code: handler of the notification of the exhaustion of the retry
#           of the timeout of the payment gateway
class PaymentGatewayTimeoutRetryExhaustionNotificationHandler:
    """Handler of the notification of the exhaustion of the retry of the
    timeout of the payment gateway."""

    def handle(self, notice) -> None:
        log.error("retry of the timeout of the payment gateway is exhausted")
```

```text
# Non-STE log line (do not write this)
paymentgatewaytimeoutretryexhaustionnotificationhandler: retry failed
```

Commit title and README:

```text
# STE-Code commit title
Update the policy of the storage bucket of the image of the avatar of the
profile of the user account

# Non-STE commit title (do not write this)
useraccountprofileavatarimagestoragebucketpolicyupdate
```

```markdown
# STE-Code README
The schedule of the reset of the window of the rate limit of the inbound
request controls the burst. Set the window to 60 seconds.
```

Code comment — head noun first, then attach the rest with `on` and `of`:

```python
# STE-Code comment: the alert suppression rule on the overflow
# of the background worker queue runs on the staging cluster
def install_alert_rule(cluster: str) -> None:
    rule = AlertSuppressionRule(on=OverflowOf(WorkerQueue(background=True)))
    deploy(rule, cluster="staging")
```

**See also:** Rule 1.3 (approved words) · Rule 1.5 (technical noun categories) ·
Rule 2.2 (long nouns in full) · Rule 2.3 (hyphens).

---

## Rule 2.2 — Write Long Technical Nouns in Full

> Source: ASD-STE100 Issue 9, Rule 2.2 · `master.md#sec2-rule2.2`.

**Rule.** When a technical code noun has more than three words, write it in
full. Then use one of these methods to make it clear:

- **Method 1** — give a shorter form or an approved abbreviation.
- **Method 2** — use prepositions (`of`, `on`, `in`, `for`, `to`) to split the
  long noun into short parts (see Rule 2.1).
- **Method 3** — use hyphens between words that you use as one unit (see Rule 2.3).

A long multi-word code noun can be one long technical noun, or a combination of
shorter technical nouns. Frequently you cannot divide it, because it is the
technical noun that your company, framework, or subject field uses. In that
case write it as it is, in its approved form.

### Method 1 — Shorter form of technical code nouns

If a long technical code noun comes from an official code document (an API
specification, a schema, an OpenAPI file, or an architecture diagram), write it
in full the first time it occurs in the text. Then, where possible, explain it
and use a shorter form or an approved abbreviation in the rest of the document.

> Before you do this procedure, initialize the user session cache invalidation
> lock handler (the handler that locks the cache of the user session, referred
> to in this procedure as the "invalidation lock handler").

Here "user session cache invalidation lock handler" is written in full; after
the explanation the shorter noun is "invalidation lock handler" — three words,
which obeys Rule 2.1.

```python
# STE-Code: write the long technical code noun in full, then use the short form
def initialize_session_lock(user_id: str) -> None:
    """Initialize the user session cache invalidation lock handler.

    The invalidation lock handler locks the cache of the user session so that
    a background job cannot read stale data while a write is in flight.
    """
    handler = UserSessionCacheInvalidationLockHandler(user_id)
    handler.engage()   # from here, refer to it as the "invalidation lock handler"

# later in the document, use the short form:
#   The invalidation lock handler releases the cache when the write is done.
```

When the surrounding text already gives all the necessary information, no extra
explanation is needed — write each official noun in full on first use, define
its abbreviation, then reuse the abbreviation:

> The Main Form Validation Module (MFVM) is a TypeScript module that includes a
> Main Export Controller Unit (MECU) and a Data Bridge (DB). The MFVM is
> installed in the application core layer and operates in the form submission
> system. The function of the MFVM is to validate and submit the form data from
> the Main Form Provider (MFP) to the data stores and the validation hooks. The
> Dynamic Config Unit (DECU) sends events to operate the MFVM.

```typescript
// STE-Code: abbreviation defined on first use, then reused
interface FormPayload { fields: Record<string, unknown>; }

class MainFormValidationModule {       // MFVM
  constructor(
    private readonly exportController: MainExportControllerUnit,  // MECU
    private readonly bridge: DataBridge,                          // DB
    private readonly config: DynamicConfigUnit,                   // DECU
  ) {}

  submit(payload: FormPayload): void {
    this.config.onEvent("submit", () => this.exportController.run(payload));
  }
}
```

If an approved technical code noun has three words or fewer, abbreviations are
not necessary. Do not fill a procedure with letter codes:

| Do not write: | WRITE: |
|---|---|
| The primary parts of the controller are: - The DTA (8) - The PVA (15) - The BA (17) - The VB (20). | A. Remove the data transformer assembly (8) from the view body (20). B. Remove the pipeline validator assembly (15) from its seat. C. Remove the buffer assembly (17) from the view body (20). |
| A. Remove the DTA (8) from the VB (20). B. Remove the PVA (15) from its seat. C. Remove the BA (17) from the VB (20). | A. Remove the data transformer assembly (8) from the view body (20). B. Remove the pipeline validator assembly (15) from its seat. C. Remove the buffer assembly (17) from the view body (20). |

```yaml
# STE-Code: name each part in full; do not pack the parts into letter codes
controller:
  data_transformer_assembly:   # (8)  part of the view body
  pipeline_validator_assembly: # (15) sits on its seat
  buffer_assembly:             # (17) part of the view body

# Non-STE (do not write this):
#   parts: [DTA_8, PVA_15, BA_17, VB_20]
```

```python
# STE-Code: write the part names in full; use the approved verb `remove`
def disassemble_controller(view_body, validator_seat):
    view_body.remove(data_transformer_assembly)         # (8)
    validator_seat.remove(pipeline_validator_assembly)  # (15)
    view_body.remove(buffer_assembly)                   # (17)
```

### Method 2 — Use prepositions to break up a long noun

When a long technical code noun is a chain of short nouns (for example, "user
authentication token refresh failure retry policy"), it is hard to read and easy
to parse the wrong way. Make the main noun the head of the sentence, then attach
the rest with `of`, `on`, `in`, `for`, or `to`.

| Non-STE (do not write) | STE-Code |
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

A 4-to-6-word noun becomes a short head noun plus prepositional phrases. This is
useful for config keys, rule names, and error-handling terms that grow long.

### Method 3 — Hyphenate words that you use as one unit

When two or more words act as a single modifier before a noun, hyphenate them so
that the reader does not group the words the wrong way. In code prose,
hyphenate compound modifiers such as `request-response`, `read-write`,
`build-time`, `out-of-band`, `end-to-end`, and `run-time`. Do not hyphenate when
the first word is an adverb ending in `-ly` ("a publicly documented API").

| Non-STE (do not write) | STE-Code |
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

Note: hyphenation groups words into one unit but does not make a long technical
noun short. If the hyphenated unit still has more than three words (for example,
"request-response mapping handler"), write it in full the first time, then use
the shorter form ("mapping handler") in the rest of the text.

### Expanded code-domain pairs

> **Non-STE:** The USCIlh must run before the shutdown hook releases the cache. If the USCIlh fails, the stale session remains.
>
> **STE:** Initialize the user session cache invalidation lock handler (the handler that locks the cache of the user session; in this procedure, we call it the "invalidation lock handler"). Run the invalidation lock handler before the shutdown hook releases the cache. If the invalidation lock handler fails, the stale session remains.

```python
# STE-Code: the long noun is written in full, then shortened for reuse
class UserSessionCacheInvalidationLockHandler:
    def engage(self) -> None: ...
    def release(self) -> None: ...

def shutdown_hook(session_id: str) -> None:
    handler = UserSessionCacheInvalidationLockHandler(session_id)
    handler.engage()          # invalidation lock handler
    if not handler.release():
        raise StaleSessionError(session_id)  # stale session remains
```

> **Non-STE:** The MFVM uses the MECU and the DB. The DECU sends events to the MFVM so that the MFVM can get data from the MFP.
>
> **STE:** The Main Form Validation Module (MFVM) is a TypeScript module that includes a Main Export Controller Unit (MECU) and a Data Bridge (DB). The Dynamic Config Unit (DECU) sends events to operate the MFVM, and the MFVM gets form data from the Main Form Provider (MFP).

```typescript
// STE-Code: abbreviation defined on first use, then reused in the text
const mfvm = new MainFormValidationModule(     // MFVM
  mecu,  // Main Export Controller Unit
  db,    // Data Bridge
  decu,  // Dynamic Config Unit
);
decu.onEvent("submit", () => mfvm.submit(mfp.getData()));  // MFP = Main Form Provider
```

> **Non-STE:** Call the DTA to configure the MFVM before you run the build, then check the MFVM output for errors.
>
> **STE:** Use the data transformer adapter to configure the main form validation module before you run the build. Then check the output of the main form validation module for errors.

```bash
# STE-Code: run the build after you configure the module
make configure MODULE=data-transformer-adapter   # data transformer adapter
make build MODULE=main-form-validation-module    # main form validation module
make test   MODULE=main-form-validation-module && echo "output checked for errors"
```

> **Non-STE:** Update the cross service request tracing correlation identifier generator after the schema change.
>
> **STE:** Update the correlation identifier generator for the tracing of the request across services after the schema change. (On first use, write "cross-service request tracing correlation identifier generator" in full, then refer to it as the "correlation identifier generator.")

```python
# STE-Code: write the long noun in full, then use the short form
def update_correlation_generator(schema: dict) -> None:
    """Update the cross-service request tracing correlation identifier generator.

    After the first use, this component is the correlation identifier generator.
    """
    CorrelationIdentifierGenerator.for_request_tracing().apply(schema)
```

> **Non-STE:** The CI pipeline docker image layer cache warming step now runs in parallel.
>
> **STE:** The cache warming step for the layer of the Docker image of the CI pipeline now runs in parallel. (On first use, write "CI pipeline Docker image layer cache warming step" in full, then refer to it as the "cache warming step.")

```yaml
# STE-Code: the step name is long on first use, then shortened in the runbook
jobs:
  warm_cache:   # cache warming step for the layer of the Docker image of the CI pipeline
    runs-on: ubuntu-latest
    strategy:
      matrix:
        layer: [base, deps, build]
    steps:
      - run: ./scripts/warm-cache.sh "${{ matrix.layer }}"
```

> **Non-STE:** Document the legacy database migration rollback failure notification webhook endpoint in the runbook.
>
> **STE:** Document the webhook endpoint for the notification of the failure of the rollback of the legacy database migration in the runbook. (On first use, write "legacy database migration rollback failure notification webhook endpoint" in full, then refer to it as the "notification webhook endpoint.")

```text
# STE-Code runbook entry
Document the webhook endpoint for the notification of the failure of the
rollback of the legacy database migration. After the first use, refer to it
as the "notification webhook endpoint" and add it to the on-call alert route.
```

### Procedure

1. Find the long technical code noun (more than three words) in your sentence.
2. Write it in full the first time it occurs. If it comes from an official
   source (API spec, schema, architecture diagram), keep the exact approved form.
3. Give a shorter form or an approved abbreviation right after the full form, in
   parentheses.
4. In the rest of the document, use only the shorter form or the abbreviation.
5. If the noun is a chain of short nouns, split it with prepositions (Rule 2.1).
6. If two or more words act as one modifier, hyphenate them (Rule 2.3).
7. Do not fill a procedure with abbreviations. A short, clear noun beats a string
   of letters.

**See also:** Rule 2.1 (three-word limit) · Rule 1.5 (noun categories and your
glossary) · Rule 1.3 (approved verbs: `use`, `set`, `get`, `make`, `show`,
`check`, `remove`, `send`, `start`, `stop`).

---

## Rule 2.3 — Use Hyphens Between Words Used as One Unit

> Source: ASD-STE100 Issue 9, Rule 2.3 · `master.md#sec2-rule2.3`.

**Rule.** A hyphen is a punctuation mark that connects words or parts of words.
Use hyphens between words to show that related words operate as one unit. This
method makes multi-word code nouns agree with Rule 2.1: hyphenated words always
count as one word, so a hyphenated code noun fills only one of the three word
slots that Rule 2.1 allows.

Constraints:

- Do not connect words that are not related — the hyphen changes the meaning of
  the multi-word code noun. If you are not sure, explain the noun in the clearest
  way, then use a shorter form, an approved verb (`get`, `set`, `make`, `start`),
  or an official abbreviation from your glossary.
- If an approved technical code noun already includes hyphens — `input-output
  stream`, `thread-safe queue`, `backward-compatible API` — do not change it. If
  it is too long, write it in full on first use, then use the shorter form.
- Do not hyphenate groups of more than three words. Keep a hyphen group to at
  most three words; split longer chains with prepositions (`of`, `on`, `in`).
- If an approved technical code noun has three words or fewer (`data adapter`,
  `pipeline validator`), hyphens are not necessary.

### Compliant examples

| Example | Note |
|---|---|
| Make sure that the fail-safe shutdown-handler connection is safe. | 3 words: make / sure / connection |
| Inspection of the request rate-limit device. | 3 words: inspection / of / device |
| The thread-safe queue keeps the order of the write operations. | 3 words: queue / keeps / order |
| Remove the backward-compatible API client before you make the change. | 3 words |

### Hyphenate the related pair only — do not chain every word

> **Non-STE:** Move the `main-feature-flag-rollback-handler` trigger to start the test run. (Reads as 2 words, but is not correct — four words joined as one unit.)
>
> **STE:** Move the `main-feature-flag` rollback-handler trigger to start the test run. (3 words: move / trigger / run)

```bash
# STE-Code compliant: the hyphen joins the related pair only
make test trigger=rollback-handler flag=main-feature-flag
```

```python
# STE: "main-feature-flag" (1 unit) + "rollback-handler" (1 unit) + "trigger" (1 unit)
def move_trigger(main_feature_flag: str, rollback_handler: str) -> None:
    """Move the main-feature-flag rollback-handler trigger to start the test run."""
    trigger = f"{main_feature_flag}:{rollback_handler}"
    start_test_run(trigger)
```

### Do not hyphenate a three-word approved technical noun

When the official name of a component is three words or fewer, leave the spaces.
Hyphenating it changes the count and can confuse the reader.

> **Non-STE:** A. Remove the `data-adapter` assembly (8) from the view body (20). B. Remove the `pipeline-validator` assembly (15) from its seat.
>
> **STE:** A. Remove the `data adapter` assembly (8) from the view body (20). B. Remove the `pipeline validator` assembly (15) from its seat.

```python
# STE: "data adapter" and "pipeline validator" are each a 2-word technical noun
def remove_assembly(name: str, part_id: int) -> None:
    """Remove the data adapter assembly (part_id) from the view body."""
    detach(name, part_id)
    log(f"removed {name} assembly {part_id}")

remove_assembly("data adapter", 8)
remove_assembly("pipeline validator", 15)
```

```text
# STE-Code migration note (descriptive)
Remove the data adapter assembly (8) from the view body (20).
Remove the pipeline validator assembly (15) from its seat.
```

### Keep a hyphen that the official name already has

If your official code documentation or an approved standard already hyphenates a
technical noun, keep the hyphen. Removing it changes the term.

> **Non-STE:** The `input output stream` is part of the logging system.
>
> **STE:** The `input-output stream` is part of the logging system.

```python
# STE: "input-output stream" keeps its hyphen because the standard defines it so
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

**See also:** Rule 2.1 (the three-word limit that hyphenated units help you
meet) · Rule 1.5 (where hyphenated code terms such as `thread-safe queue` and
`backward-compatible API` are defined) · Rule 2.2 (pair hyphenated nouns with
short approved verbs such as `make`, `get`, `set`, `start`, `remove`).

---

## Checklist for Section 2

- [ ] No noun phrase has more than three words (a hyphenated unit counts as one).
- [ ] Noun chains are split at ownership points with `of`, `on`, `in`, or `for`.
- [ ] Every noun longer than three words is written in full on first use, with a
      shorter form or approved abbreviation given in parentheses.
- [ ] The rest of the document uses only the short form.
- [ ] Hyphens join related pairs only, never four or more words.
- [ ] Official hyphenated terms keep their hyphens; three-word approved nouns
      keep their spaces.
- [ ] Instruction text uses approved verbs only.
