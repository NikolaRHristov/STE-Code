# Rule 2.2 — Write Long Technical Nouns in Full

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.2

> **Source:** [master.md#sec2-rule2.2](ste-code/grouped/)

> Source: master.md#sec2-rule2.2

## Original Rule

### Rule 2.2 When a technical noun has more than three words, write it in full.

When a technical noun has more than three words, write it in full. Then, you can use one of these methods to make the technical noun clear:

- Give a shorter form of the technical noun.
- Use hyphens (-) between words that you use as one unit.

A long multi-word noun can be a long technical noun, or it can be a combination of shorter technical nouns. Frequently, it is not possible to divide technical nouns into smaller parts because they are the technical nouns that your company, industry, or subject field uses. Thus, you must write technical nouns as they are, in their approved form.

#### Method 1 - Shorter form of technical nouns

If a long technical noun comes from an official document (for example, an engineering drawing or an illustrated parts catalog), write it in full the first time that it occurs in the text. Then, if it is possible, explain the technical noun and in the remaining text of your document, use a shorter form or an approved abbreviation.

#### Examples in STE

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

## Adapted Rule

When a technical code noun has more than three words, write it in full. Then, use one of these methods to make the technical noun clear:

- Give a shorter form of the technical code noun.
- Use hyphens (-) between words that you use as one unit.

A long multi-word code noun can be a long technical noun, or it can be a combination of shorter technical nouns. Frequently, it is not possible to divide technical code nouns into smaller parts because they are the technical nouns that your company, framework, or subject field uses. Thus, you must write technical code nouns as they are, in their approved form.

### Method 1 - Shorter form of technical code nouns

If a long technical code noun comes from an official code document (for example, an API specification, a schema, or an architecture diagram), write it in full the first time that it occurs in the text. Then, if it is possible, explain the technical code noun and in the remaining text of your document, use a shorter form or an approved abbreviation.

#### Examples in STE-Code

Before you do this procedure, initialize the user session cache invalidation lock handler (the handler that locks the cache of the user session, referred to in this procedure as the "invalidation lock handler").

In this example, you write "user session cache invalidation lock handler" in full. Then, after an explanation, you give a shorter technical code noun: "invalidation lock handler." This shorter technical code noun has three words and obeys rule 2.1.

The Main Form Validation Module (MFVM) is a TypeScript module that includes a Main Export Controller Unit (MECU) and a Data Bridge (DB). The MFVM is installed in the application core layer and operates in the form submission system. The function of the MFVM is to validate and submit the form data from the Main Form Provider (MFP) to the data stores and the validation hooks. The Dynamic Config Unit (DECU) sends events to operate the MFVM.

In this example, the explanation is not necessary because the text gives all the necessary information about the module. You write all official technical code nouns that include more than three nouns in full the first time that they occur. Then, in the remaining parts of the text, you use their related approved abbreviations.

If an approved technical code noun includes three words or less, it is not necessary to use abbreviations.

#### Example

| Do not write: | WRITE: |
|---|---|
| The primary parts of the controller are: - The DTA (8) - The PVA (15) - The BA (17) - The VB (20). | A. Remove the data transformer assembly (8) from the view body (20). B. Remove the pipeline validator assembly (15) from its seat. C. Remove the buffer assembly (17) from the view body (20). |

You can use abbreviations that come from your official code documentation but be careful. A text full of abbreviations in a procedure, although shorter, is not easy to read.

#### Example

| Do not write: | WRITE: |
|---|---|
| A. Remove the DTA (8) from the VB (20). B. Remove the PVA (15) from its seat. C. Remove the BA (17) from the VB (20). | A. Remove the data transformer assembly (8) from the view body (20). B. Remove the pipeline validator assembly (15) from its seat. C. Remove the buffer assembly (17) from the view body (20). |

### Code-domain example pair

> **Non-STE:** Use the DTA to configure the MFVM before you run the build.
>
> **STE:** Use the data transformer adapter to configure the main form validation module before you run the build.
>
> *Adaptation note: Write the long technical code noun in full the first time it occurs. Then use the approved abbreviation in the remaining text.*
