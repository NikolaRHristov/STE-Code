# Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.1

## Original Rule

**Rule 8.1** You can use all standard English punctuation marks but not the semicolon (;).

The semicolon (;) is not permitted in STE because it lets you write very long sentences. It is also not easy to use correctly. As an alternative to the semicolon, always write two different sentences.

Examples:

| **Non-STE:** | (1) Examine the removed parts; replace the damaged ones. |

| **STE:** | (1) Examine the removed parts for damage. |

| | (2) Replace the damaged part(s). |

## STE-Code Adaptation

**Rule 8.1** In code documentation, you can use all standard English punctuation marks but not the semicolon (;).

The semicolon (;) is not permitted in STE-Code because it lets you write very long sentences that are difficult to read in code comments and documentation. It is also not easy to use correctly. As an alternative to the semicolon, always write two different sentences.

### Examples

> **Non-STE:** Call the function to parse the response data; handle any errors that occur.
> **STE:** Call the function to parse the response data. Handle any errors that occur.
>
> *Adapted from spec pair: "Examine the removed parts; replace the damaged ones." → split into two sentences.*

> **Non-STE:** The cache is invalid after a write operation; you must flush it before the next read.
> **STE:** The cache is invalid after a write operation. You must flush it before the next read.
>
> *Adapted from spec pair: "Examine the removed parts; replace the damaged ones." → split into two sentences.*
