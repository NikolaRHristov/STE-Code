# Rule 2.2 — Long Technical Nouns (Shorter Forms and Hyphens)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.2

## Original Rule

When a technical noun has more than three words, write it in full. Then, you can use one of these methods to make the technical noun clear:

- Give a shorter form of the technical noun.
- Use hyphens (-) between words that you use as one unit.

A long multi-word noun can be a long technical noun, or it can be a combination of shorter technical nouns. Frequently, it is not possible to divide technical nouns into smaller parts because they are the technical nouns that your company, industry, or subject field uses. Thus, you must write technical nouns as they are, in their approved form.

### Method 1 – Shorter form of technical nouns

If a long technical noun comes from an official document (for example, an engineering drawing or an illustrated parts catalog), write it in full the first time that it occurs in the text. Then, if it is possible, explain the technical noun and in the remaining text of your document, use a shorter form or an approved abbreviation.

**Examples in STE:**

Before you do this procedure, engage the ramp service door safety connector pin (the pin that holds the ramp service door, referred to in this procedure as the "safety connector pin").

In this example, you write "ramp service door safety connector pin" in full. Then, after an explanation, you give a shorter technical noun: "safety connector pin." This shorter technical noun has three words and obeys rule 2.1.

The Main Fuel Metering Unit (MFMU) is an aluminum alloy unit that includes a Main Engine Control Unit (MECU) and a Distribution Block (DB). The MFMU is installed in the engine bypass duct and operates in the engine fuel system. The function of the MFMU is to meter and supply the fuel from the Main Engine Fuel Pump (MEFP) to the fuel manifolds and the starter jets. The Digital Engine Control Unit (DECU) sends electrical signals to operate the MFMU.

In this example, the explanation is not necessary because the text gives all the necessary information about the unit. You write all official technical nouns that include more than three nouns in full the first time that they occur. Then, in the remaining parts of the text, you use their related approved abbreviations.

If an approved technical noun includes three words or less, it is not necessary to use abbreviations.

Example:

> **Do not write:**
> The primary parts of the valve are:
> - The DA (8)
> - The PVA (15)
> - The BA (17)
> - The VB (20).
>
> **Write:**
> The primary parts of the valve are:
> - The diaphragm assembly (8)
> - The poppet valve assembly (15)
> - The bush assembly (17)
> - The valve body (20).

You can use abbreviations that come from your official company documentation but be careful. A text full of abbreviations in a procedure, although shorter, is not easy to read.

### Method 2 — Hyphens (-) between the words that you use as one unit

A hyphen is a punctuation mark that connects words or parts of words. You can use hyphens between words to show how related words operate as one unit. This method will make the multi-word nouns that you use agree with rule 2.1. Hyphenated words always count as one word.

Examples in STE:

Make sure that the cutoff-switch power connection is safe. (3 words)

Inspection of the lavatory rapid-decompression device. (3 words)

Make sure that you do not connect words which are not related, because this hyphen will change the meaning of the multi-word noun. If you are not sure, only explain the multi-word noun. Then, use a shorter form, or an official approved abbreviation.

If an approved technical noun includes hyphens, do not change it. If it is too long, write it in full the first time it occurs and then use the recommended method (shorter technical nouns) specified in this rule.

Do not use hyphens to make groups of more than three words. If you use hyphens for all the words, this multi-word noun will not be easy to read and understand.

Example:

> **Non-STE:** Move the main-gear-door-retraction-winch handle. (2 words, but not correct)
> **STE:** Move the main-gear-door retraction-winch handle. (3 words)

If an approved technical noun includes three words or less (for example "poppet valve assembly" and "diaphragm assembly"), it is not necessary to use hyphens.

Example:

> **Do not write:**
> A. Remove the diaphragm-assembly (8) from the valve body (20).
> B. Remove the poppet-valve assembly (15) from its seat.
>
> **Write:**
> A. Remove the diaphragm assembly (8) from the valve body (20).
> B. Remove the poppet valve assembly (15) from its seat.

But, if an approved technical noun includes a hyphen (for example "inward-outward valve"), do not remove the hyphen. Keep the technical noun that comes from your official company documentation.

## STE-Code Adaptation

In code documentation, some technical terms have more than three words and cannot be broken down because they are the official names used by your company, programming language, framework, or subject field. Examples include formal class names, design pattern names, official API names, or names from architecture diagrams.

### Method 1 – Shorter form of technical nouns

Write the long technical noun in full the first time it occurs. Provide an explanation, then use a shorter form or the official abbreviation in the remaining text. Do not abbreviate technical nouns that already have three words or fewer.

### Method 2 — Hyphens

Use hyphens to group related words that function as a single unit within a multi-word noun. A hyphenated group counts as one word. Do not hyphenate words that are not related, and do not create hyphenated groups of more than three words. If an official technical noun already contains a hyphen (for example, from the source code or framework documentation), keep the hyphen.

### Examples

**Method 1 – Shorter form with explanation:**

> **Non-STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler.
> **STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler (the component that authenticates requests in the middleware pipeline, referred to in this document as the "authentication handler").

In this example, you write "HTTP request pipeline middleware authentication handler" in full. Then, after an explanation, you give a shorter technical noun: "authentication handler." This shorter technical noun has three words and obeys rule 2.1.

> **See also:** Rule 2.1 — Multi-word Nouns (Maximum Three Words)

**Method 1 – Shorter form with official abbreviation:**

> **Non-STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler.
> **STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler (the component that authenticates requests in the middleware pipeline, referred to in this document as the "authentication handler").
>
> The Object Relational Mapping (ORM) layer is a middleware component that includes a Query Builder (QB) and a Unit of Work (UoW) manager. The ORM layer operates in the data access pipeline and manages persistence for the domain model. The QB constructs database queries from the domain object graph. The UoW manager tracks changes to entities during a transaction.

**Method 1 – Do not abbreviate short technical nouns (three words or fewer):**

> **Non-STE:**
> The primary parts of the system are:
> - The CM (8)
> - The EB (15)
> - The CR (17)
> - The DTL (20).
>
> **STE:**
> The primary parts of the system are:
> - The cache manager (8)
> - The event bus (15)
> - The command router (17)
> - The data transfer layer (20).

This shorter technical noun has three words and obeys rule 2.1.

> **See also:** Rule 2.1 — Multi-word Nouns (Maximum Three Words)

**Method 2 – Hyphens between related words:**

> **Non-STE:** Move the data-access-layer-query-builder interface. (2 words, but not correct)
> **STE:** Move the data-access-layer query-builder interface. (3 words)

**Method 2 – Do not add hyphens to short approved technical nouns:**

> **Non-STE:**
> A. Remove the cache-manager (8) from the service container (20).
> B. Remove the event-bus (15) from its listener.
>
> **STE:**
> A. Remove the cache manager (8) from the service container (20).
> B. Remove the event bus (15) from its listener.

**Method 2 – Keep official hyphens from approved terms:**

> **Non-STE:**
> A. Remove the cache manager (8) from the service container (20). (removes the official hyphen from a framework term)
> B. Remove the read write lock (15) from its mutex. (removes the official hyphen from a concurrency primitive)
>
> **STE:**
> A. Remove the cache-manager (8) from the service container (20). (keeps the official hyphen from the framework documentation)
> B. Remove the read-write lock (15) from its mutex. (keeps the official hyphen from the concurrency library)
