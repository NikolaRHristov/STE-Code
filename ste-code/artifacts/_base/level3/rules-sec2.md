<!-- a-sec2-rule2.1.md -->

# Rule 2.1 — Keep Technical Nouns Short

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.1
> **Spec reference:** [master.md#sec2-rule2.1](ste-code/grouped/) (pages 60–63 of 434)
> **Domain:** Code documentation — API docs, commit messages, README sections, code comments
> **Alphabetical key:** 2 · **Group:** 005-rules-sec-2

## Original Rule

To keep multi-word nouns short, you can use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word nouns.

> The four pairs below are the ASD-STE100 source examples. They show the pattern in the aerospace domain. The STE-Code examples later in this file re-express the same pattern for code documentation. Keep them only as the traceable source; do not copy the aerospace terms into STE-Code guidance.

#### Examples (ASD-STE100 source)

> **Non-STE:** _Runway light connection resistance calibration._ (5 words)
>
> **STE:** Calibration of the resistance of the runway light connection. (1 word, 1 word, and 3 words)
>
> **Non-STE:** _Install the forward turbine overheat thermocouple terminal tags._ (6 words)
>
> **STE:** Install the terminal tags on the forward overheat thermocouple of the turbine. (2 words and 3 words)
>
> **Non-STE:** _Remove the engine transmission housing attachment bolts._ (5 words)
>
> **STE:** Remove the bolts that attach the transmission housing to the engine. (1 word, 1 word, 2 words, and 1 word)
>
> **Non-STE:** _Adjust to obtain door operating rod alignment with the attachment point._ (4 words)
>
> **STE:** Adjust the door operating rod until it aligns with the attachment point. (3 words and 1 word)

## Adapted Rule

To keep multi-word technical nouns short, use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word technical nouns. Write each multi-word technical noun as a short noun that uses prepositions to make the meaning clear. A technical noun that the code domain uses (for example, a module name, a class name, a configuration key, an endpoint path, an error type, or a test fixture) must stay short so that the reader can parse it without effort.

When a phrase names a code component with more than a few words, break the phrase into small nouns that connect with prepositions. Do not write one long noun that stacks modifiers. Explain the relationship between the parts with "of," "on," "in," or "for."

Why this matters in code documentation:

- A reader scans docs fast. A stacked noun such as `authentication_token_expiration_refresh_interval_setting` hides which part owns which. A short noun with prepositions shows the tree: the setting belongs to the interval, the interval belongs to the expiration, the expiration belongs to the token.
- Short technical nouns match how code is already structured. A config key, a class, or a JSON field is one short concept. Prepositions in the sentence show how those short concepts relate.
- Follow the Microsoft and Google style guides: use short, plain words. Do not use `utilize`, `leverage`, or `employ` when `use` is enough. Do not use `commence`, `initiate`, or `terminate` when `start` and `stop` are enough. Keep the verb simple and the noun short.
- Approved code-domain adjectives stay attached to the short noun they modify: `idempotent`, `immutable`, `thread-safe`, `atomic`, `nullable`, `deprecated`, `stateless`, `backward-compatible`, `asynchronous`, `concurrent`, `deterministic`. Write `the idempotent retry policy`, not `idempotentretrypolicy`.

How to apply the rule:

1. Find a noun that stacks two or more modifiers (a "noun chain").
2. Split the chain at the ownership or containment points.
3. Connect the parts with `of`, `on`, `in`, or `for`.
4. If a part is itself a code component, name it with its short technical noun (its class, key, or file), not a merged word.
5. In instruction text, use the approved verbs: `set`, `get`, `make`, `show`, `check`, `remove`, `send`, `start`, `stop`, `use`, `update`. Do not use `configure` for `set`, `retrieve` for `get`, `delete`/`purge` for `remove`, or `display` for `show`.

### Examples in STE-Code

> *Adapted from spec pair:* Non-STE: Runway light connection resistance calibration. | STE: Calibration of the resistance of the runway light connection.

The pairs below re-express the ASD-STE100 pattern for code documentation. Each pair shows a full, runnable situation: a long stacked noun (Non-STE) and the same idea written as short nouns with prepositions (STE), followed by the code, config, API doc, test, or commit message that the documentation describes.

#### 1. Configuration key — auth token refresh

> **Non-STE:** Authentication token expiration refresh interval setting
>
> **STE:** Setting of the refresh interval of the expiration of the authentication token

A doc that names the config as one long chain forces the reader to decode the ownership tree. Write the key as short nested nouns and state the relationship with `of`.

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

#### 2. Deployment labels — middleware config

> **Non-STE:** Install the forward service request validator middleware config tags.
>
> **STE:** Install the config tags on the validator middleware of the request of the forward service.

A setup guide that stacks the component path into one noun makes the target unclear. Name the target with prepositions so the reader knows what the tag goes on.

```bash
# STE-Code: the tag goes on the validator middleware of the request of the forward service
kubectl label pods \
  -l app=forward-service \
  middleware=validator \
  config=enabled
```

```yaml
# Non-STE: one long noun, unclear where the tag applies (do not write this)
install_forward_service_request_validator_middleware_config_tags: true
```

#### 3. Cleanup task — migration lock files

> **Non-STE:** Remove the database migration script output directory lock files.
>
> **STE:** Remove the lock files that lock the output directory of the migration script of the database.

A runbook step that names the file as a chain is hard to search and hard to parse. State the ownership with `of` and use the approved verb `remove` (not `delete` or `purge` in instruction text).

```python
# STE-Code: remove the lock files that lock the output directory
#            of the migration script of the database
from pathlib import Path

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
# Test that checks the cleanup (use `check`, not `verify`)
def test_remove_migration_lock_files(tmp_path):
    out = tmp_path / "app" / "output"
    out.mkdir(parents=True)
    (out / "write.lock").write_text("")
    count = remove_migration_lock_files("app")
    assert count == 1
    assert not any(out.glob("*.lock"))
```

#### 4. Test setup — cache hook alignment

> **Non-STE:** Adjust to obtain cache invalidation hook alignment with the event emitter.
>
> **STE:** Adjust the cache invalidation hook until it aligns with the event emitter.

A test helper that stacks the alignment target is vague. Name the hook, then state what it aligns with.

```python
# STE-Code: adjust the cache invalidation hook until it aligns with the event emitter
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

#### 5. API documentation — retry policy

> **Non-STE:** Payment gateway timeout retry exhaustion notification handler.
>
> **STE:** Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway.

An API doc, error type, or log line that stacks five nouns is hard to grep and hard to read. Split it so each level is a short noun.

```python
# STE-Code: handler of the notification of the exhaustion of the retry
#            of the timeout of the payment gateway
class PaymentGatewayTimeoutRetryExhaustionNotificationHandler:
    """Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway."""

    def handle(self, notice) -> None:
        log.error("retry of the timeout of the payment gateway is exhausted")
```

```text
# Non-STE log line (do not write this)
paymentgatewaytimeoutretryexhaustionnotificationhandler: retry failed
```

#### 6. Commit message — schema change

> **Non-STE:** User account profile avatar image storage bucket policy update.
>
> **STE:** Update of the policy of the storage bucket of the image of the avatar of the profile of the user account.

A commit title that stacks the path is unclear about what changed. Use the approved verb `update` (or `make`/`set`) and show ownership with `of`.

```text
# STE-Code commit title
Update the policy of the storage bucket of the image of the avatar of the profile of the user account

# Non-STE commit title (do not write this)
useraccountprofileavatarimagestoragebucketpolicyupdate
```

#### 7. README section — rate limit

> **Non-STE:** The inbound request rate limit window reset schedule controls the burst.
>
> **STE:** The schedule of the reset of the window of the rate limit of the inbound request controls the burst.

A README sentence that stacks the noun hides what the schedule actually resets. Name the short nouns and connect them with `of`.

```markdown
# STE-Code README

The schedule of the reset of the window of the rate limit of the inbound
request controls the burst. Set the window to 60 seconds.
```

```yaml
# Non-STE: one long key, unclear what resets (do not write this)
inbound_request_rate_limit_window_reset_schedule: "*/1 * * * *"
```

#### 8. Code comment — background job

> **Non-STE:** The background worker queue overflow alert suppression rule runs on the staging cluster.
>
> **STE:** The alert suppression rule on the overflow of the background worker queue runs on the staging cluster.

A code comment that stacks the subject makes the reader re-read. Put the head noun first, then attach the rest with `on` and `of`.

```python
# STE-Code comment: the alert suppression rule on the overflow
# of the background worker queue runs on the staging cluster
def install_alert_rule(cluster: str) -> None:
    rule = AlertSuppressionRule(on=OverflowOf(WorkerQueue(background=True)))
    deploy(rule, cluster="staging")
```

## See also

> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Code-Domain Technical Noun Category (what counts as a technical noun in code documentation)
> **See also:** Rule 1.3 — Use Approved Words Only with Their Approved Meanings (keep verbs and nouns plain: use, set, get, remove, check, update, show)
> **See also:** Rule 2.2 — Write Long Technical Nouns in Full (when a noun must stay long, write it in full then use a short form)
> **See also:** Rule 2.3 — Use Hyphens Between Words Used as One Unit (hyphenate a related pair, but do not chain more than three words)

---

<!-- a-sec2-rule2.2.md -->

# Rule 2.2 — Write Long Technical Nouns in Full

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.2

> **Source:** [master.md#sec2-rule2.2](ste-code/grouped/)

> Source: master.md#sec2-rule2.2

## Original Rule

> *The block below is the ASD-STE100 source verbatim, kept for traceability. It uses aerospace terms. Do not copy those terms into STE-Code guidance; the Adapted Rule section re-expresses the same pattern for code documentation.*

### Rule 2.2 When a technical noun has more than three words, write it in full.

When a technical noun has more than three words, write it in full. Then, you can use one of these methods to make the technical noun clear:

- Give a shorter form of the technical noun.
- Use hyphens (-) between words that you use as one unit.

A long multi-word noun can be a long technical noun, or it can be a combination of shorter technical nouns. Frequently, it is not possible to divide technical nouns into smaller parts because they are the technical nouns that your company, industry, or subject field uses. Thus, you must write technical nouns as they are, in their approved form.

#### Method 1 - Shorter form of technical nouns

If a long technical noun comes from an official document (for example, an engineering drawing or an illustrated parts catalog), write it in full the first time that it occurs in the text. Then, if it is possible, explain the technical noun and in the remaining text of your document, use a shorter form or an approved abbreviation.

#### Examples in STE

> *Adapted from spec pair:* Non-STE: "Runway light connection resistance calibration." (5-word noun) | STE: "Calibration of the resistance of the runway light connection."

<mark>Before you do this procedure, engage the ramp service door safety connector pin (the pin that hold the ramp service door, referred to in this procedure as the "safety connector pin".</mark>

In this example, you write "ramp service door safety connector pin" in full. Then, after an explanation, you give a shorter technical noun: "safety connector pin." This shorter technical noun has three words and obeys rule 2.1.

> <mark>The Main Fuel Metering Unit (MFMU) is an aluminum alloy unit that includes a Main Engine Control Unit (MECU) and a Distribution Block (DB). The MFMU is installed in the engine bypass duct and operates in the engine fuel system. The function of the MFMU is to meter and supply the fuel from the Main Engine Fuel Pump (MEFP) to the fuel manifolds and the starter jets. The Digital Engine Control Unit (DECU) sends electrical signals to operate the MFMU. </mark>

In this example, the explanation is not necessary because the text gives all the necessary information about the unit. You write all official technical nouns that include more than three nouns in full the first time that they occur. Then, in the remaining parts of the text, you use their related approved abbreviations.

If an approved technical noun includes three words or less, it is not necessary to use abbreviations.

#### Example

| Do not write: | WRITE: |
|---|---|
| The primary parts of the valve are: - The DA (8) - The PVA (15) - The BA (17) - The VB (20). | A. Remove the diaphragm assembly (8) from the valve body (20). B. Remove the poppet valve assembly (15) from its seat. C. Remove the bush assembly (17) from the valve body (20). |

You can use abbreviations that come from your official company documentation but be careful. A text full of abbreviations in a procedure, although shorter, is not easy to read.

#### Example

| Do not write: | WRITE: |
|---|---|
| A. Remove the DA (8) from the VB (20). B. Remove the PVA (15) from its seat. C. Remove the BA (17) from the VB (20). | A. Remove the diaphragm assembly (8) from the valve body (20). B. Remove the poppet valve assembly (15) from its seat. C. Remove the bush assembly (17) from the valve body (20). |

## STE-Code Adaptation

When a technical code noun has more than three words, write it in full. Then, use one of these methods to make the technical code noun clear:

- Give a shorter form of the technical code noun.
- Use hyphens (-) between words that you use as one unit.
- Use prepositions (for example, "of," "on," "in," "for," and "to") to split a long noun into short, separate parts (see Rule 2.1).

A long multi-word code noun can be a long technical noun, or it can be a combination of shorter technical nouns. Frequently, it is not possible to divide technical code nouns into smaller parts because they are the technical nouns that your company, framework, or subject field uses. Thus, you must write technical code nouns as they are, in their approved form.

> *Adapted from spec pair:* Non-STE: "Runway light connection resistance calibration." (5-word noun) | STE: "Calibration of the resistance of the runway light connection."

### Method 1 - Shorter form of technical code nouns

If a long technical code noun comes from an official code document (for example, an API specification, a schema, an OpenAPI file, or an architecture diagram), write it in full the first time that it occurs in the text. Then, if it is possible, explain the technical code noun and in the remaining text of your document, use a shorter form or an approved abbreviation.

#### Examples in STE-Code

Before you do this procedure, initialize the user session cache invalidation lock handler (the handler that locks the cache of the user session, referred to in this procedure as the "invalidation lock handler").

In this example, you write "user session cache invalidation lock handler" in full. Then, after an explanation, you give a shorter technical code noun: "invalidation lock handler." This shorter technical code noun has three words and obeys rule 2.1.

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

The Main Form Validation Module (MFVM) is a TypeScript module that includes a Main Export Controller Unit (MECU) and a Data Bridge (DB). The MFVM is installed in the application core layer and operates in the form submission system. The function of the MFVM is to validate and submit the form data from the Main Form Provider (MFP) to the data stores and the validation hooks. The Dynamic Config Unit (DECU) sends events to operate the MFVM.

In this example, the explanation is not necessary because the text gives all the necessary information about the module. You write all official technical code nouns that include more than three nouns in full the first time that they occur. Then, in the remaining parts of the text, you use their related approved abbreviations.

```typescript
// STE-Code: abbreviation defined on first use, then reused
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

If an approved technical code noun includes three words or less, it is not necessary to use abbreviations.

#### Example — parts list with a config object

| Do not write: | WRITE: |
|---|---|
| The primary parts of the controller are: - The DTA (8) - The PVA (15) - The BA (17) - The VB (20). | A. Remove the data transformer assembly (8) from the view body (20). B. Remove the pipeline validator assembly (15) from its seat. C. Remove the buffer assembly (17) from the view body (20). |

You can use abbreviations that come from your official code documentation but be careful. A text full of abbreviations in a procedure, although shorter, is not easy to read.

```yaml
# STE-Code: name each part in full; do not pack the parts into letter codes
controller:
  data_transformer_assembly:   # (8)  part of the view body
  pipeline_validator_assembly: # (15) sits on its seat
  buffer_assembly:             # (17) part of the view body

# Non-STE (do not write this):
#   parts: [DTA_8, PVA_15, BA_17, VB_20]
```

#### Example — step list with code

| Do not write: | WRITE: |
|---|---|
| A. Remove the DTA (8) from the VB (20). B. Remove the PVA (15) from its seat. C. Remove the BA (17) from the VB (20). | A. Remove the data transformer assembly (8) from the view body (20). B. Remove the pipeline validator assembly (15) from its seat. C. Remove the buffer assembly (17) from the view body (20). |

```python
# STE-Code: write the part names in full; use the approved verb `remove`
def disassemble_controller(view_body, validator_seat):
    view_body.remove(data_transformer_assembly)   # (8)
    validator_seat.remove(pipeline_validator_assembly)  # (15)
    view_body.remove(buffer_assembly)              # (17)
```

### Method 2 - Use prepositions to break up a long noun

When a long technical code noun is a chain of short nouns (for example, "user authentication token refresh failure retry policy"), it is hard to read and easy to parse the wrong way. You can keep the meaning and obey the rule by making the main noun the head of the sentence, then adding the rest with prepositions. Put the key noun first, then attach the modifiers with "of," "on," "in," "for," or "to." This makes each part short while the full idea stays clear.

#### Examples in STE-Code

> **Non-STE:** Configure the user authentication token refresh failure retry policy before you deploy the service to production.
>
> **STE:** Configure the retry policy for the failure of the refresh of the user authentication token before you deploy the service to production.

> **Non-STE:** Install the background worker queue overflow alert suppression rule on the staging cluster.
>
> **STE:** Install the alert suppression rule on the overflow of the background worker queue on the staging cluster.

> **Non-STE:** Remove the database connection pool exhaustion recovery timeout configuration parameter from the settings file.
>
> **STE:** Remove the configuration parameter that sets the recovery timeout for the exhaustion of the database connection pool from the settings file.

```python
# STE-Code: the short noun keeps the function name and the docstring clear
def set_recovery_timeout(pool, seconds: float) -> None:
    """Set the configuration parameter that sets the recovery timeout
    for the exhaustion of the database connection pool."""
    pool.config["recovery_timeout_seconds"] = seconds
```

> **Non-STE:** Update the build script to obtain output directory naming consistency with the package convention.
>
> **STE:** Update the build script until the output directory naming is consistent with the package convention.

These four pairs follow the same pattern as the ASD-STE100 source: a 4-to-6-word noun becomes a short head noun plus prepositional phrases. In code documentation this is useful for config keys, rule names, and error-handling terms that tend to grow long.

### Method 3 - Hyphenate words that you use as one unit

When two or more words act as a single modifier before a noun, use a hyphen (-) to show that they are one unit. This stops the reader from grouping the words the wrong way. In code prose, hyphenate compound modifiers such as "request-response," "read-write," "build-time," "out-of-band," "end-to-end," and "run-time." Do not hyphenate the modifier when the first word is an adverb that ends in "-ly" (for example, "a publicly documented API" stays open).

#### Examples in STE-Code

> **Non-STE:** Set the request response mapping handler to the new schema before the migration.
>
> **STE:** Set the request-response mapping handler to the new schema before the migration.

> **Non-STE:** Run the build time configuration check after you compile the module.
>
> **STE:** Run the build-time configuration check after you compile the module.

> **Non-STE:** Add an end to end test for the payment flow before you merge the change.
>
> **STE:** Add an end-to-end test for the payment flow before you merge the change.

> **Non-STE:** Use the out of band signal to stop the long running job.
>
> **STE:** Use the out-of-band signal to stop the long-running job.

```python
# STE-Code: hyphenated modifiers are one unit in code identifiers too
def handle_request_response(handler: "RequestResponseMappingHandler") -> None:
    """Set the request-response mapping handler to the new schema."""
    handler.apply(schema=SCHEMA_V2)

def run_build_time_check() -> None:
    """Run the build-time configuration check after you compile the module."""
    ...
```

Note: Hyphenation groups words into one unit but does not make a long technical noun short. If the hyphenated unit still has more than three words (for example, "request-response mapping handler"), write it in full the first time, then use the shorter form ("mapping handler") in the rest of the text.

### Code-domain example pairs (expanded)

The pairs below show full, realistic documentation situations. Each Non-STE line breaks the rule; each STE line writes the long code noun in full first, then uses the shorter form or abbreviation. Each pair is followed by the runnable code, config, or test that the documentation describes.

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
>
> *Adaptation note: Write the long technical code noun in full the first time it occurs. Then use the approved abbreviation, defined on first use, in the rest of the text.*

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

### How to apply the rule in code documentation

1. Find the long technical code noun (more than three words) in your sentence.
2. Write it in full the first time it occurs. If it comes from an official source (API spec, schema, architecture diagram), keep the exact approved form.
3. Give a shorter form or an approved abbreviation right after the full form, in parentheses.
4. In the rest of the document, use only the shorter form or the approved abbreviation.
5. If the noun is a chain of short nouns, split it with prepositions so each part is short (see Rule 2.1).
6. If two or more words act as one modifier, hyphenate them.
7. Do not fill a procedure with abbreviations. A short, clear noun is better than a string of letters.

> **Microsoft / Google style note:** Use short, plain words. Do not use `utilize`, `leverage`, or `employ` when `use` is enough. Do not use `commence`, `initiate`, or `terminate` when `start` and `stop` are enough. Keep the verb simple and the noun short.

> **See also:** Rule 2.1 — Keep Technical Nouns to Three Words or Fewer · Rule 1.5 — Technical Noun Categories and Your Company Glossary · Rule 1.3 — Use Approved Words (use, set, get, make, show, check, remove, send, start, stop)

---

<!-- a-sec2-rule2.3.md -->

# Rule 2.3 — Use Hyphens Between Words Used asdf One Unit

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.3

> **Source:** [master.md#sec2-rule2.3](ste-code/grouped/)

> Source: master.md#sec2-rule2.3

## Original Rule

#### Method 2 - Hyphens (-) between the words that you use as one unit

A hyphen is a punctuation mark that connects words or parts of words. You can use hyphens between words to show how related words operate as one unit. This method will make the multi-word nouns that you use agree with rule 2.1. Hyphenated words always count as one word.

##### Examples in STE

| Example | Note |
|---|---|
| Make sure that the cutoff-switch power connection is safe. | (3 words) |
| Inspection of the lavatory rapid-decompression device. | (3 words) |

Make sure that you do not connect words which are not related, because this hyphen will change the meaning of the multi-word noun. If you are not sure, only explain the multi-word noun. Then, use a shorter form, or an official approved abbreviation.

If an approved technical noun includes hyphens, do not change it. If it is too long, write it in full the first time it occurs and then use the recommended method (shorter technical nouns) specified in this rule.

Do not use hyphens to make groups of more than three words. If you use hyphens for all the words, this multi-word noun will not be easy to read and understand.

##### Example

> **Non-STE:** Move the main-gear-door-retraction-winch handle. (2 words, but not correct)
>
> **STE:** Move the main-gear-door retraction-winch handle. (3 words)

If an approved technical noun includes three words or less (for example "poppet valve assembly" and "diaphragm assembly"), it is not necessary to use hyphens.

##### Example

| Do not write: | WRITE: |
|---|---|
| A. Remove the diaphragm-assembly (8) from the valve body (20). B. Remove the poppet-valve assembly (15) from its seat. | A. Remove the diaphragm assembly (8) from the valve body (20). B. Remove the poppet valve assembly (15) from its seat. |

But, if an approved technical noun includes a hyphen (for example "inward-outward valve"), do not remove the hyphen. Keep the technical noun that comes from your official company documentation.

##### Example

> **Non-STE:** <u><mark>Do not write: The inward outward valve is part of the fuel system.</mark></u>
>
> **STE:** <mark>WRITE: The inward-outward valve is part of the fuel system.</mark>

> *Adapted from spec pair:* Non-STE: Move the main-gear-door-retraction-winch handle. (2 words, but not correct)  |  STE: Move the main-gear-door retraction-winch handle. (zip 3 words)

## Adapted Rule

A hyphen is a punctuation mark that connects words or parts of words. Use hyphens between words to show how related words operate as one unit. This method will make the multi-word code nouns that you use agree with rule 2.1. Hyphenated words always count as one word, so a hyphenated code noun fills only one of the three-word slots that rule 2.1 allows for a noun phrase.

Do not connect words that are not related, because the hyphen will change the meaning of the multi-word code noun. If you are not sure, only explain the multi-word code noun in the clearest way. Then, use a shorter form, an approved verb such as `get`, `set`, `make`, `start`, or an official approved abbreviation from your glossary.

If an approved technical code noun includes hyphens — for example `input-output stream`, `thread-safe queue`, or `backward-compatible API` — do not change it. If it is too long, write it in full the first time it occurs and then use the recommended method for shorter technical nouns that this rule specifies.

Do not use hyphens to make groups of more than three words. If you hyphenate all the words, this multi-word code noun will not be easy to read and understand. Keep the hyphen group to at most three words; split longer chains with prepositions such as `of`, `on`, or `in`.

### Examples in STE-Code

> *Adapted from spec pair:* Non-STE: Move the main-feature-flag-rollback-handler trigger.  |  STE: Move the main-feature-flag rollback-handler trigger.

| Example | Note |
|---|---|
| Make sure that the fail-safe shutdown-handler connection is safe. | (3 words: make / sure / connection) |
| Inspection of the request rate-limit device. | (3 words: inspection / of / device) |
| The thread-safe queue keeps the order of the write operations. | (3 words: queue / keeps / order) |
| Remove the backward-compatible API client before you make the change. | ( susceptible 3 words) |

When a hyphen joins two related words, the pair counts as one unit. Apply this in procedural and descriptive code documentation so that the reader can parse the noun without re-reading it.

#### Full example — hyphenate related words, keep to three words

A README step that names a combined component must keep the three-word limit of rule 2.1. Hyphenate only the related pair; do not chain every word.

> **Non-STE:** Move the `main-feature-flag-rollback-handler` trigger to start the test run. (2 words, but not correct — four words joined as one unit)
>
> **STE:** Move the `main-feature-flag` rollback-handler trigger to start the test run. (3 words: move / trigger / run)

Run the matching test to check the result:

```bash
# STE-Code compliant: the hyphen joins the related pair only
make test trigger=rollback-handler flag=main-feature-flag
```

```python
# STE: the multi-word noun is "main-feature-flag" (1 unit) + "rollback-handler" (1 unit) + "trigger" (1 unit)
def move_trigger(main_feature_flag: str, rollback_handler: str) -> None:
    """Move the main-feature-flag rollback-handler trigger to start the test run."""
    trigger = f"{main_feature_flag}:{rollback_handler}"
    start_test_run(trigger)
```

#### Full example — do not hyphenate a three-word approved technical noun

When the official name of a component is three words or less, leave the spaces. Hyphenating it changes the count and can confuse the reader.

> **Non-STE:** A. Remove the `data-adapter` assembly (8) from the view body (20). B. Remove the `pipeline-validator` assembly (15) from its seat.
>
> **STE:** A. Remove the `data adapter` assembly (8) from the view body (20). B. Remove the `pipeline validator` assembly (15) from its seat.

```python
# STE: "data adapter" and "pipeline validator" are each a 2-word technical noun, not hyphenated
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

#### Full example — keep a hyphen that the official name already has

If your official code documentation or an approved standard already hyphenates a technical noun, keep the hyphen. Removing it changes the term.

> **Non-STE:** Do not write: The `input output stream` is part of the logging system.
>
> **STE:** WRITE: The `input-output stream` is part of the logging system.

```python
# STE: "input-output stream" keeps its hyphen because the standard defines it that way
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

> **See also:** Rule 2.1 — Write Nouns as Nouns and Keep Noun Phrases to Three Words (the three-word limit that hyphenated units help you meet)
> **See also:** Rule 1.5 — Use Technical Nouns from the Approved Categories (where hyphenated code terms such as `thread-safe queue` and `backward-compatible API` are defined)
> **See also:** Rule 2.2 — Use Approved Verbs and Keep Sentences Short (pair hyphenated nouns with short approved verbs such as `make`, `get`, `set`, `start`, `remove`)
