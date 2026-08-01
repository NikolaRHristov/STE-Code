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
