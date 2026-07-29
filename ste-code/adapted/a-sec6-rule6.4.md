# Rule 6.4 — Use Paragraphs to Show Related Information

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.4

## Original Rule

In procedures, work steps usually have numbers and letters to show their sequence. In descriptive writing, paragraphs keep related information together and give a logical sequence to the text.

In STE, a paragraph starts with a "topic sentence" which tells the reader about the topic of that paragraph. Then, the sentences that follow the topic sentence explain it, or give more information related to it.

## STE-Code Adaptation

In code documentation, procedures such as setup instructions usually have numbered steps to show their sequence. In descriptive code documentation, paragraphs keep related information together and give a logical sequence to the text.

In STE-Code, a paragraph starts with a "topic sentence" which tells the reader about the topic of that paragraph. Then, the sentences that follow the topic sentence explain it, or give more information related to it. When a new paragraph starts, the reader knows that there will be a new topic or different information in that paragraph.

### Examples

The example that follows describes an error handling system in a code documentation context. The topic sentence at the start of each paragraph tells the reader what the paragraph explains. More information follows gradually and connects correctly to the information in the text.

> **STE-Code:**
>
> 1. Error Handler Component
>
> A. General
>
> (1) The Error Handler component catches errors that occur during the execution of the application. The component catches errors from these sources:
> - The HTTP request layer
> - The data access layer
> - The message queue consumers
> - The scheduled task runners
> - The third-party API integrations
> - The authentication middleware.
>
> (2) From the source location, the Error Handler component traces the error through the call stack of the application. A high volume of errors can cause a decrease in the performance of the application. Thus, a temporary or a permanent failure of the logging service and the monitoring dashboard can occur.
>
> (3) If an error occurs in the production environment, it is necessary to examine the error logs for the root cause. The operations team must do this examination before the next deployment.

The topic sentences are:
- Paragraph (1): "The Error Handler component catches errors that occur during the execution of the application."
- Paragraph (2): "From the source location, the Error Handler component traces the error through the call stack of the application."
- Paragraph (3): "If an error occurs in the production environment, it is necessary to examine the error logs for the root cause."

Each topic sentence introduces the subject of its paragraph. The sentences that follow each topic sentence add more information about that subject.
