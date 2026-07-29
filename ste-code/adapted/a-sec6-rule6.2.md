# Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.2

## Original Rule

Key words are words that occur in a text to connect different ideas, and key phrases are phrases that have the same function.

These key words and key phrases show how information in a text is related and give the text a logical structure.

You can also use connecting words and connecting phrases to help the reader understand the logical flow of ideas in the text. Connecting words and connecting phrases have the function of traffic signs, which tell the reader if the information is new, different, or a result of previous information. Examples of approved connecting words are: "and," "but," "then," "thus," and examples of connecting phrases are "as a result," and "at the same time."

When you use key words and key phrases, make sure that you do not change them in your text. The same terminology will keep your text clear and correct.

## STE-Code Adaptation

In code documentation, key words are technical terms that connect different ideas across sentences, and key phrases are groups of words that have the same function. Use the same technical terms consistently throughout your documentation. Do not switch between synonyms such as "function," "method," and "routine" for the same concept.

Key words and key phrases show how information in code documentation is related and give the text a logical structure. When you describe a class, an API, a data flow, or a system component, reuse the same key words in consecutive sentences to connect related ideas. Connecting words such as "and," "but," "then," and "thus" and connecting phrases such as "as a result" and "at the same time" help the reader follow the logical flow.

### Examples

The example that follows is the STE-Code text from the adaptation of Rule 6.1. The key words and key phrases connect each sentence to the next and give the text a logical structure. Sentences are numbered 1 through 10 for reference.

**Sentence 1 and Sentence 2:**

> Sentence 1: The Data Processing Service (the service) receives input from three sources.
> Sentence 2: The three sources are the message queue, the REST API endpoints, and the scheduled batch jobs.

Sentence 2 uses the key phrase "three sources" from Sentence 1 again and adds more information about what those sources are.

**Sentence 2 and Sentence 3:**

> Sentence 2: The three sources are the message queue, the REST API endpoints, and the scheduled batch jobs.
> Sentence 3: The service processes the input data through a pipeline that has three stages.

Sentence 3 uses the key words "service" and "three" again. It introduces the new concept of "pipeline" and "three stages."

**Sentence 3 and Sentence 4:**

> Sentence 3: The service processes the input data through a pipeline that has three stages.
> Sentence 4: The three stages are validation, transformation, and enrichment.

Sentence 4 uses the key phrase "three stages" from Sentence 3 again and adds the names of each stage.

**Sentence 4 and Sentences 5 and 6:**

> Sentence 4: The three stages are validation, transformation, and enrichment.
> Sentence 5: The validation stage uses the rule engine.
> Sentence 6: The transformation stage uses the reference data cache.

Sentences 5 and 6 each reuse one key word from Sentence 4: "validation" becomes "validation stage" and "transformation" becomes "transformation stage." Each sentence adds one new subject: the rule engine and the reference data cache.

**Paragraph 1 and Paragraph 2:**

> Paragraph 1 (Sentences 1 through 6): pipeline, three stages, service
> Paragraph 2 (Sentences 7 through 10): The service writes the output to the target database. The service then publishes a completion event to the event stream. The Notification Service and the Reporting Module consume these events to update their internal state. The service loads its processing rules from the configuration store at startup. The service also sends throughput data and error counts to the metrics collector. The operations team uses the monitoring dashboard to read this data.

Paragraph 2 uses the key word "service" from Paragraph 1 again to maintain the logical connection between the paragraphs. It also uses the key phrase "processing rules" which connects back to "rule engine" in Sentence 5.
