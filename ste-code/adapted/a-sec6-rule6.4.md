# Rule 6.4 — Use Paragraphs to Show Related Information

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.4

## Original Rule

In procedures, work steps usually have numbers and letters to show their sequence. In descriptive writing, paragraphs keep related information together and give a logical sequence to the text.

In STE, a paragraph starts with a "topic sentence" which tells the reader about the topic of that paragraph. Then, the sentences that follow the topic sentence explain it, or give more information related to it.

In the example, the underlined topic sentence at the start of each paragraph helps the reader understand the content of the paragraph and its topic. When a new paragraph starts, the reader knows that there will be a new topic or different information in that paragraph.

## STE-Code Adaptation

In procedures, work steps usually have numbers and letters to show their sequence. In descriptive code documentation, paragraphs keep related information together and give a logical sequence to the text.

In STE-Code, a paragraph starts with a "topic sentence" which tells the developer about the topic of that paragraph. Then, the sentences that follow the topic sentence explain it, or give more information related to it.

The topic sentence at the start of each paragraph helps the developer understand the content of the paragraph and its topic. When a new paragraph starts, the developer knows that there will be a new topic or different information in that paragraph.

### Examples

> **Non-STE:** The data pipeline processes incoming events through a sequence of stages. Each stage transforms the event payload and passes it to the next stage. The first stage is validation, which checks the event schema and rejects malformed events. The second stage is enrichment, which adds metadata such as timestamps, source identifiers, and geolocation data from an external lookup service. The third stage is transformation, which converts the event into the target format required by downstream consumers such as the analytics warehouse and the real-time dashboard. The final stage is persistence, which writes the transformed event to the primary data store and to the event log for audit purposes. Error handling is implemented at each stage to catch exceptions without breaking the entire pipeline. If a stage fails, the pipeline logs the error and routes the event to the dead-letter queue for manual inspection.

> **STE:**
>
> **1. Data Pipeline Overview**
>
> The data pipeline processes incoming events through a sequence of stages. Each stage transforms the event payload and passes it to the next stage. Error handling is implemented at each stage to catch exceptions without breaking the pipeline. If a stage fails, the pipeline logs the error and routes the event to the dead-letter queue for manual inspection.
>
> **2. Validation Stage**
>
> The first stage is validation. This stage checks the event schema. It rejects events that are malformed.
>
> **3. Enrichment Stage**
>
> The second stage is enrichment. This stage adds metadata to the event:
> - Timestamps
> - Source identifiers
> - Geolocation data from an external lookup service.
>
> **4. Transformation Stage**
>
> The third stage is transformation. This stage converts the event into the target format. Downstream consumers use this format. These consumers include:
> - The analytics warehouse
> - The real-time dashboard.
>
> **5. Persistence Stage**
>
> The final stage is persistence. This stage writes the transformed event to two destinations. It writes the event to the primary data store. It also writes the event to the event log for audit purposes.
>
> *Code-domain example — each paragraph starts with a topic sentence and keeps related information together, giving the documentation a logical sequence.*

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic
