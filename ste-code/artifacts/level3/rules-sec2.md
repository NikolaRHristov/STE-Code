# Level 3 — Section 2: Technical Noun Rules (2.1–2.3)

Distilled reference for LLMs that generate code documentation. These three
rules govern how to write multi-word technical nouns so they stay short, clear,
and parseable. All examples are code-domain. Adapted from ASD-STE100 Issue 9.

Scope of this slice:
- Rule 2.1 — Keep Technical Nouns Short
- Rule 2.2 — Write Long Technical Nouns in Full
- Rule 2.3 — Use Hyphens Between Words Used as One Unit

Core idea shared by all three: a technical noun phrase (a class name, config
key, endpoint path, error type, test fixture, or commit subject) should stay
short — ideally three words or fewer. When it must be longer, write it in full
once, then use a short form or abbreviation. Use prepositions (`of`, `on`,
`in`, `for`, `to`) to break ownership chains, and hyphens only to glue related
words into one unit.

## Rule 2.1 — Keep Technical Nouns Short

**Source:** ASD-STE100 Issue 9, Rule 2.1 (adapted for code documentation).

### Rule
To keep multi-word technical nouns short, use prepositions (`of`, `on`, `in`,
`for`) and explain the noun instead of stacking modifiers. A code component that
is a technical noun — a module name, class name, config key, endpoint path,
error type, or test fixture — must stay short so the reader parses it without
effort.

Split a noun chain at its ownership/containment points and connect the parts
with prepositions. Do not write one long noun that stacks modifiers.

### Why it matters
- A reader scans docs fast. A stacked noun such as
  `authentication_token_expiration_refresh_interval_setting` hides which part
  owns which. Prepositions reveal the tree.
- Short technical nouns match how code is already structured: a config key,
  class, or JSON field is one short concept; prepositions show how concepts
  relate.
- Use short plain words (Microsoft/Google style): `use` not `utilize`/`leverage`
  /`employ`; `start`/`stop` not `commence`/`initiate`/`terminate`.
- Approved code-domain adjectives stay attached to the short noun they modify:
  `idempotent`, `immutable`, `thread-safe`, `atomic`, `nullable`, `deprecated`,
  `stateless`, `backward-compatible`, `asynchronous`, `concurrent`,
  `deterministic`. Write `the idempotent retry policy`, not `idempotentretrypolicy`.

### How to apply
1. Find a noun that stacks two or more modifiers (a "noun chain").
2. Split the chain at ownership/containment points.
3. Connect parts with `of`, `on`, `in`, or `for`.
4. Name each code component by its short technical noun (class, key, file),
   not a merged word.
5. In instruction text use approved verbs: `set`, `get`, `make`, `show`,
   `check`, `remove`, `send`, `start`, `stop`, `use`, `update`. Do not use
   `configure` for `set`, `retrieve` for `get`, `delete`/`purge` for `remove`,
   or `display` for `show`.

### Examples in STE-Code

**1. Configuration key — auth token refresh**
- Non-STE: Authentication token expiration refresh interval setting
- STE: Setting of the refresh interval of the expiration of the authentication token

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
def get_refresh_interval(token):
    """Return the setting of the refresh interval of the expiration of the authentication token."""
    return token.expiration.refresh_interval_seconds
```

**2. Deployment labels — middleware config**
- Non-STE: Install the forward service request validator middleware config tags.
- STE: Install the config tags on the validator middleware of the request of the forward service.

```bash
# the tag goes on the validator middleware of the request of the forward service
kubectl label pods -l app=forward-service middleware=validator config=enabled
```

```yaml
# Non-STE (do not write this)
install_forward_service_request_validator_middleware_config_tags: true
```

**3. Cleanup task — migration lock files**
- Non-STE: Remove the database migration script output directory lock files.
- STE: Remove the lock files that lock the output directory of the migration script of the database.

```python
def remove_migration_lock_files(db_name: str) -> int:
    """Remove the lock files that lock the output directory of the migration script of the database."""
    output_dir = Path("migrations") / db_name / "output"
    removed = 0
    for lock in output_dir.glob("*.lock"):
        lock.unlink()
        removed += 1
    return removed
```

```python
def test_remove_migration_lock_files(tmp_path):
    out = tmp_path / "app" / "output"
    out.mkdir(parents=True)
    (out / "write.lock").write_text("")
    count = remove_migration_lock_files("app")
    assert count == 1
    assert not any(out.glob("*.lock"))
```

**4. Test setup — cache hook alignment**
- Non-STE: Adjust to obtain cache invalidation hook alignment with the event emitter.
- STE: Adjust the cache invalidation hook until it aligns with the event emitter.

```python
def align_cache_hook(hook, emitter, timeout: float = 5.0) -> bool:
    """Adjust the cache invalidation hook until it aligns with the event emitter."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if hook.target is emitter:
            return True
        hook.nudge()
    return False
```

**5. API documentation — retry policy**
- Non-STE: Payment gateway timeout retry exhaustion notification handler.
- STE: Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway.

```python
class PaymentGatewayTimeoutRetryExhaustionNotificationHandler:
    """Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway."""

    def handle(self, notice) -> None:
        log.error("retry of the timeout of the payment gateway is exhausted")
```

**6. Commit message — schema change**
- Non-STE: User account profile avatar image storage bucket policy update.
- STE: Update of the policy of the storage bucket of the image of the avatar of the profile of the user account.

```text
# STE-Code commit title
Update the policy of the storage bucket of the image of the avatar of the profile of the user account

# Non-STE commit title (do not write this)
useraccountprofileavatarimagestoragebucketpolicyupdate
```

**7. README section — rate limit**
- Non-STE: The inbound request rate limit window reset schedule controls the burst.
- STE: The schedule of the reset of the window of the rate limit of the inbound request controls the burst.

```markdown
The schedule of the reset of the window of the rate limit of the inbound
request controls the burst. Set the window to 60 seconds.
```

**8. Code comment — background job**
- Non-STE: The background worker queue overflow alert suppression rule runs on the staging cluster.
- STE: The alert suppression rule on the overflow of the background worker queue runs on the staging cluster.

```python
def install_alert_rule(cluster: str) -> None:
    rule = AlertSuppressionRule(on=OverflowOf(WorkerQueue(background=True)))
    deploy(rule, cluster="staging")
```

### See also
- Rule 1.5 — Technical Noun Categories (what counts as a technical noun).
- Rule 1.3 — Use Approved Words Only (keep verbs/nouns plain).
- Rule 2.2 — Write Long Technical Nouns in Full.
- Rule 2.3 — Use Hyphens Between Words Used as One Unit.

## Rule 2.2 — Write Long Technical Nouns in Full

**Source:** ASD-STE100 Issue 9, Rule 2.2 (adapted for code documentation).

### Rule
When a technical code noun has more than three words, write it in full the
first time it occurs. Then use one of these methods to make it clear:
- Give a shorter form of the technical code noun.
- Use hyphens (`-`) between words used as one unit (see Rule 2.3).
- Use prepositions (`of`, `on`, `in`, `for`, `to`) to split a long noun into
  short, separate parts (see Rule 2.1).

A long multi-word code noun can be one long technical noun, or a combination of
shorter ones. When the noun is an official term your company, framework, or
subject field uses, you must write it in its approved form — even if you cannot
split it.

### Method 1 — Shorter form / abbreviation
If a long technical code noun comes from an official code document (API spec,
schema, OpenAPI file, architecture diagram), write it in full the first time it
occurs. Then, if possible, give a shorter form or approved abbreviation in
parentheses, and reuse that form in the rest of the document.

- Write "user session cache invalidation lock handler" in full, then refer to
  it as the "invalidation lock handler" (3 words, obeys Rule 2.1).
- Approved abbreviations from official code docs are allowed, but a text full
  of abbreviations is hard to read. If an approved noun is three words or less,
  do not abbreviate.

```python
def initialize_session_lock(user_id: str) -> None:
    """Initialize the user session cache invalidation lock handler.

    The invalidation lock handler locks the cache of the user session so that
    a background job cannot read stale data while a write is in flight.
    """
    handler = UserSessionCacheInvalidationLockHandler(user_id)
    handler.engage()   # from here, refer to it as the "invalidation lock handler"
```

Abbreviation defined on first use, then reused:

```typescript
// The Main Form Validation Module (MFVM) is a TypeScript module that
// includes a Main Export Controller Unit (MECU) and a Data Bridge (DB).
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

Parts list — name each part in full; do not pack parts into letter codes:

```yaml
controller:
  data_transformer_assembly:   # (8)  part of the view body
  pipeline_validator_assembly: # (15) sits on its seat
  buffer_assembly:             # (17) part of the view body

# Non-STE (do not write this):
#   parts: [DTA_8, PVA_15, BA_17, VB_20]
```

```python
def disassemble_controller(view_body, validator_seat):
    view_body.remove(data_transformer_assembly)        # (8)
    validator_seat.remove(pipeline_validator_assembly) # (15)
    view_body.remove(buffer_assembly)                  # (17)
```

### Method 2 — Prepositions to break a long noun
When a long noun is a chain of short nouns (e.g. "user authentication token
refresh failure retry policy"), make the main noun the head of the sentence and
attach the rest with prepositions. Put the key noun first, then add modifiers
with `of`, `on`, `in`, `for`, `to`.

- Non-STE: Configure the user authentication token refresh failure retry policy before you deploy the service to production.
- STE: Configure the retry policy for the failure of the refresh of the user authentication token before you deploy the service to production.

- Non-STE: Install the background worker queue overflow alert suppression rule on the staging cluster.
- STE: Install the alert suppression rule on the overflow of the background worker queue on the staging cluster.

- Non-STE: Remove the database connection pool exhaustion recovery timeout configuration parameter from the settings file.
- STE: Remove the configuration parameter that sets the recovery timeout for the exhaustion of the database connection pool from the settings file.

```python
def set_recovery_timeout(pool, seconds: float) -> None:
    """Set the configuration parameter that sets the recovery timeout
    for the exhaustion of the database connection pool."""
    pool.config["recovery_timeout_seconds"] = seconds
```

- Non-STE: Update the build script to obtain output directory naming consistency with the package convention.
- STE: Update the build script until the output directory naming is consistent with the package convention.

### Method 3 — Hyphenate words used as one unit
When two or more words act as a single modifier before a noun, use a hyphen to
show they are one unit. Hyphenate compound modifiers such as `request-response`,
`read-write`, `build-time`, `out-of-band`, `end-to-end`, `run-time`. Do NOT
hyphenate when the first word is an `-ly` adverb (e.g. "a publicly documented
API" stays open).

- Non-STE: Set the request response mapping handler to the new schema before the migration.
- STE: Set the request-response mapping handler to the new schema before the migration.

- Non-STE: Run the build time configuration check after you compile the module.
- STE: Run the build-time configuration check after you compile the module.

- Non-STE: Add an end to end test for the payment flow before you merge the change.
- STE: Add an end-to-end test for the payment flow before you merge the change.

- Non-STE: Use the out of band signal to stop the long running job.
- STE: Use the out-of-band signal to stop the long-running job.

```python
def handle_request_response(handler: "RequestResponseMappingHandler") -> None:
    """Set the request-response mapping handler to the new schema."""
    handler.apply(schema=SCHEMA_V2)

def run_build_time_check() -> None:
    """Run the build-time configuration check after you compile the module."""
    ...
```

Note: hyphenation groups words into one unit but does not make a long technical
noun short. If the hyphenated unit still has more than three words (e.g.
"request-response mapping handler"), write it in full the first time, then use
the shorter form ("mapping handler") afterward.

### Expanded code-domain example pairs
Each Non-STE line breaks the rule; each STE line writes the long noun in full,
then uses the shorter form or abbreviation.

- Non-STE: The USCIlh must run before the shutdown hook releases the cache. If the USCIlh fails, the stale session remains.
- STE: Initialize the user session cache invalidation lock handler (the handler that locks the cache of the user session; in this procedure, we call it the "invalidation lock handler"). Run the invalidation lock handler before the shutdown hook releases the cache. If the invalidation lock handler fails, the stale session remains.

```python
class UserSessionCacheInvalidationLockHandler:
    def engage(self) -> None: ...
    def release(self) -> None: ...

def shutdown_hook(session_id: str) -> None:
    handler = UserSessionCacheInvalidationLockHandler(session_id)
    handler.engage()          # invalidation lock handler
    if not handler.release():
        raise StaleSessionError(session_id)  # stale session remains
```

- Non-STE: The MFVM uses the MECU and the DB. The DECU sends events to the MFVM so that the MFVM can get data from the MFP.
- STE: The Main Form Validation Module (MFVM) is a TypeScript module that includes a Main Export Controller Unit (MECU) and a Data Bridge (DB). The Dynamic Config Unit (DECU) sends events to operate the MFVM, and the MFVM gets form data from the Main Form Provider (MFP).

```typescript
const mfvm = new MainFormValidationModule(     // MFVM
  mecu,  // Main Export Controller Unit
  db,    // Data Bridge
  decu,  // Dynamic Config Unit
);
decu.onEvent("submit", () => mfvm.submit(mfp.getData()));  // MFP = Main Form Provider
```

- Non-STE: Call the DTA to configure the MFVM before you run the build, then check the MFVM output for errors.
- STE: Use the data transformer adapter to configure the main form validation module before you run the build. Then check the output of the main form validation module for errors.

```bash
make configure MODULE=data-transformer-adapter   # data transformer adapter
make build MODULE=main-form-validation-module    # main form validation module
make test   MODULE=main-form-validation-module && echo "output checked for errors"
```

- Non-STE: Update the cross service request tracing correlation identifier generator after the schema change.
- STE: Update the correlation identifier generator for the tracing of the request across services after the schema change. (On first use, write "cross-service request tracing correlation identifier generator" in full, then refer to it as the "correlation identifier generator.")

```python
def update_correlation_generator(schema: dict) -> None:
    """Update the cross-service request tracing correlation identifier generator.

    After the first use, this component is the correlation identifier generator.
    """
    CorrelationIdentifierGenerator.for_request_tracing().apply(schema)
```

- Non-STE: The CI pipeline docker image layer cache warming step now runs in parallel.
- STE: The cache warming step for the layer of the Docker image of the CI pipeline now runs in parallel. (On first use, write "CI pipeline Docker image layer cache warming step" in full, then refer to it as the "cache warming step.")

```yaml
jobs:
  warm_cache:   # cache warming step for the layer of the Docker image of the CI pipeline
    runs-on: ubuntu-latest
    strategy:
      matrix:
        layer: [base, deps, build]
    steps:
      - run: ./scripts/warm-cache.sh "${{ matrix.layer }}"
```

- Non-STE: Document the legacy database migration rollback failure notification webhook endpoint in the runbook.
- STE: Document the webhook endpoint for the notification of the failure of the rollback of the legacy database migration in the runbook. (On first use, write "legacy database migration rollback failure notification webhook endpoint" in full, then refer to it as the "notification webhook endpoint.")

```text
Document the webhook endpoint for the notification of the failure of the
rollback of the legacy database migration. After the first use, refer to it
as the "notification webhook endpoint" and add it to the on-call alert route.
```

### How to apply in code documentation
1. Find the long technical code noun (more than three words) in your sentence.
2. Write it in full the first time it occurs. If it comes from an official
   source (API spec, schema, architecture diagram), keep the exact approved form.
3. Give a shorter form or approved abbreviation right after the full form, in parentheses.
4. In the rest of the document, use only the shorter form or the abbreviation.
5. If the noun is a chain of short nouns, split it with prepositions (Rule 2.1).
6. If two or more words act as one modifier, hyphenate them (Rule 2.3).
7. Do not fill a procedure with abbreviations. A short, clear noun beats a
   string of letters.

> Microsoft/Google style note: use short plain words — `use` not
> `utilize`/`leverage`/`employ`; `start`/`stop` not `commence`/`initiate`/`terminate`.

### See also
- Rule 2.1 — Keep Technical Nouns Short.
- Rule 1.5 — Technical Noun Categories and Your Company Glossary.
- Rule 1.3 — Use Approved Words (use, set, get, make, show, check, remove, send, start, stop).

## Rule 2.3 — Use Hyphens Between Words Used as One Unit

**Source:** ASD-STE100 Issue 9, Rule 2.3 (adapted for code documentation).

### Rule
A hyphen connects words or parts of words. Use hyphens between words to show
how related words operate as one unit. This keeps multi-word code nouns within
the three-word limit of Rule 2.1. A hyphenated word counts as one word, so it
fills only one of the three slots a noun phrase may use.

- Do NOT connect unrelated words with a hyphen — it changes the meaning of the
  multi-word noun. If unsure, explain the noun plainly, then use a shorter form
  or an approved abbreviation.
- If an approved technical code noun already includes hyphens — e.g.
  `input-output stream`, `thread-safe queue`, `backward-compatible API` — keep
  the hyphen. Do not change official terms.
- Do NOT use hyphens to make groups of more than three words. Keep the hyphen
  group to at most three words; split longer chains with prepositions
  (`of`, `on`, `in`).

### Examples in STE-Code

| Example | Note |
|---|---|
| Make sure that the fail-safe shutdown-handler connection is safe. | (3 words: make / sure / connection) |
| Inspection of the request rate-limit device. | (3 words: inspection / of / device) |
| The thread-safe queue keeps the order of the write operations. | (3 words: queue / keeps / order) |
| Remove the backward-compatible API client before you make the change. | (3 words) |

When a hyphen joins two related words, the pair is one unit. Apply this in
procedural and descriptive code docs so the reader parses the noun without
re-reading.

**Full example — hyphenate related words, keep to three words**
- Non-STE: Move the `main-feature-flag-rollback-handler` trigger to start the test run. (2 words, but not correct — four words joined as one unit)
- STE: Move the `main-feature-flag` rollback-handler trigger to start the test run. (3 words: move / trigger / run)

```bash
# the hyphen joins the related pair only
make test trigger=rollback-handler flag=main-feature-flag
```

```python
def move_trigger(main_feature_flag: str, rollback_handler: str) -> None:
    """Move the main-feature-flag rollback-handler trigger to start the test run."""
    trigger = f"{main_feature_flag}:{rollback_handler}"
    start_test_run(trigger)
```

**Full example — do not hyphenate a three-word approved technical noun**
When the official name is three words or less, leave the spaces. Hyphenating it
changes the count and confuses the reader.
- Non-STE: A. Remove the `data-adapter` assembly (8) from the view body (20). B. Remove the `pipeline-validator` assembly (15) from its seat.
- STE: A. Remove the `data adapter` assembly (8) from the view body (20). B. Remove the `pipeline validator` assembly (15) from its seat.

```python
def remove_assembly(name: str, part_id: int) -> None:
    """Remove the data adapter assembly (part_id) from the view body."""
    detach(name, part_id)
    log(f"removed {name} assembly {part_id}")

remove_assembly("data adapter", 8)
remove_assembly("pipeline validator", 15)
```

**Full example — keep a hyphen the official name already has**
If official code docs or an approved standard already hyphenates a term, keep
the hyphen. Removing it changes the term.
- Non-STE: The `input output stream` is part of the logging system.
- STE: The `input-output stream` is part of the logging system.

```python
class LoggingSystem:
    def __init__(self, stream: "InputOutputStream") -> None:
        # The input-output stream is part of the logging system.
        self.stream = stream

    def write(self, message: str) -> None:
        self.stream.push(message)
```

```yaml
logging:
  # The input-output stream is part of the logging system.
  input-output-stream:
    buffer-size: 4096
    flush-on-error: true
```

### See also
- Rule 2.1 — Keep Technical Nouns Short (the three-word limit hyphenated units help you meet).
- Rule 1.5 — Use Technical Nouns from the Approved Categories (where hyphenated code terms such as `thread-safe queue` and `backward-compatible API` are defined).
- Rule 2.2 — Write Long Technical Nouns in Full (pair hyphenated nouns with short approved verbs such as `make`, `get`, `set`, `start`, `remove`).

<!-- END-SEC2-4 -->



