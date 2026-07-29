# Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.5

## Original Rule

In descriptive writing, paragraphs describe topics, and it is important that each paragraph has only one topic. The topic sentence is the first and most important sentence in a paragraph. The topic sentence gives new information and makes a logical connection between the new information and previous information. To make a logical connection in a paragraph, the topic sentence usually contains a key word and/or a connecting word or connecting phrase.

From the topic sentences, the reader will understand the contents of your text and will find the applicable information quickly. If the reader writes down each of the topic sentences from a text, they will make a good outline of its content. The other sentences in each paragraph give the information a logical structure and add more information on the topic of the paragraph.

## STE-Code Adaptation

In code documentation, paragraphs describe topics, and it is important that each paragraph has only one topic. The topic sentence is the first and most important sentence in a paragraph. The topic sentence gives new information and makes a logical connection between the new information and previous information. To make a logical connection in a paragraph, the topic sentence usually contains a key word from the previous paragraph or a connecting word or connecting phrase such as "then," "thus," or "as a result."

From the topic sentences, the developer will understand the content of your documentation and will find the applicable information quickly. If the developer writes down each of the topic sentences from a text, they will make a good outline of the content. The other sentences in each paragraph give the information a logical structure and add more information on the topic of the paragraph.

### Examples

If you refer to the STE-Code text in the examples for Rules 6.1 and 6.2, you can see that the text is divided into two paragraphs:

- Paragraph 1 (sentences 1 through 6) — The topic is: "How the Data Processing Service receives and processes input."
- Paragraph 2 (sentences 7 through 10) — The topic is: "How the service writes output and reports its status."

In the example that follows, the topic sentence at the start of each paragraph helps the developer understand the content that the paragraph explains. More information then follows gradually and connects correctly to the information in the text.

> **STE-Code:**
>
> Data Processing Service
>
> The Data Processing Service (the service) receives input from three sources. The three sources are the message queue, the REST API endpoints, and the scheduled batch jobs. The service processes the input data through a pipeline that has three stages. The three stages are validation, transformation, and enrichment. The validation stage uses the rule engine. The transformation stage uses the reference data cache.
>
> After the pipeline completes, the service writes the output to the target database. The service then publishes a completion event to the event stream. The Notification Service and the Reporting Module consume these events to update their internal state. The service loads its processing rules from the configuration store at startup. The service also sends throughput data and error counts to the metrics collector. The operations team uses the monitoring dashboard to read this data.

Paragraph 1 has one topic: the input sources and processing pipeline of the service. Paragraph 2 has one topic: the output, events, configuration, and monitoring of the service. The connecting phrase "After the pipeline completes" at the start of Paragraph 2 makes a logical connection to the processing stages described in Paragraph 1.
