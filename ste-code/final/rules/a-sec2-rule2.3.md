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
