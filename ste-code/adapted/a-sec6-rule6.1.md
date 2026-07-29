# Rule 6.1 — Give Information Gradually

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.1

## Original Rule

In a descriptive text, give information gradually and make sure that each sentence contains only one subject. If you give too much information too quickly, your text will not be easy to understand, and it will be necessary for the reader to read it again.

## STE-Code Adaptation

In code documentation, give information gradually and make sure that each sentence contains only one subject. When you describe a function, a module, a data flow, or a system architecture, do not put multiple unrelated subjects in the same sentence. If you give too much information too quickly, your text will not be easy to understand, and the developer will need to read it again.

Break a complex description into logical groups. Use one sentence per subject and let each sentence add one new piece of information that builds on the previous sentence.

### Examples

The non-STE example below describes a data processing service. It packs the system overview, input sources, processing steps, output format, and transport layer into a single dense paragraph. The STE-Code text divides the same information into two paragraphs with a logical progression: the first paragraph describes the service and its inputs, and the second paragraph describes the data flow and output.

> **Non-STE:** The Data Processing Service receives input from the message queue, the REST API endpoints, and the scheduled batch jobs, processes this data through a pipeline of validation, transformation, and enrichment stages that use the rule engine and the reference data cache, and then writes the processed output to the target database and publishes completion events to the event stream which the downstream Notification Service and Reporting Module consume to update their internal state. The service uses the configuration store to load processing rules at startup and the metrics collector to record throughput and error counts to the monitoring dashboard for the operations team.

> **STE-Code:** The Data Processing Service (the service) receives input from three sources. The three sources are the message queue, the REST API endpoints, and the scheduled batch jobs. The service processes the input data through a pipeline that has three stages. The three stages are validation, transformation, and enrichment. The validation stage uses the rule engine. The transformation stage uses the reference data cache.
>
> After the pipeline completes, the service writes the output to the target database. The service then publishes a completion event to the event stream. The Notification Service and the Reporting Module consume these events to update their internal state. The service loads its processing rules from the configuration store at startup. The service also sends throughput data and error counts to the metrics collector. The operations team uses the monitoring dashboard to read this data.
