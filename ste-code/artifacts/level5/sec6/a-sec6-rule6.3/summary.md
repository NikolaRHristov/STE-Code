# Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.

## Original Rule Summary

Rule 6.3 requires that descriptive writing use a maximum of 25 words per sentence. Short sentences give a clear structure to technical writing and make information easier to understand. Descriptive text is more complex than procedural text, so the 25-word limit applies strictly to all descriptive content. Long sentences can combine multiple pieces of information in ways that obscure meaning and increase the reader's cognitive load.

## STE-Code Adaptation

Rule 6.3 in STE-Code applies the 25-word maximum to all code documentation: README files, API reference docs, docstrings, commit messages, error messages, and inline comments. Code documentation is descriptive text, not procedural text, so the 25-word limit is mandatory. Long sentences in code documentation hide important details inside dense clauses and make it hard for developers to scan for specific information. Splitting a long sentence into multiple short sentences, each describing one concept, makes code documentation more scannable, more translatable, and easier to understand for both native and non-native English readers.

## Example Pairs

> **Non-STE:** The `migrateDatabase` function connects to the source and target databases, compares their schemas to detect any structural differences, and then generates the SQL migration scripts that will bring the target database into alignment with the source schema. (37 words)
>
> **STE:** The `migrateDatabase` function connects to the source database. It connects to the target database. It compares the two schemas. It finds structural differences. It then makes SQL migration scripts. These scripts align the target schema with the source schema. (8, 6, 5, 4, 6, 10 words)
>
> *(P3 applied: the 37-word sentence is split into six sentences, each under 25 words; P4 applied: each sentence describes one function behavior — connection, comparison, detection, generation, alignment)*

>
> **Non-STE:** The GET /api/v1/reports endpoint returns a JSON array of report objects that includes metadata such as the report author, creation timestamp, and status field, and also supports pagination through the `page` and `per_page` query parameters with a default page size of 20. (42 words)
>
> **STE:** The GET /api/v1/reports endpoint returns a JSON array of report objects. Each object includes metadata about the report. The metadata includes the author, creation timestamp, and status. Use the `page` and `per_page` query parameters for pagination. The default page size is 20. (11, 7, 9, 9, 6 words)
>
> *(P12 applied: API docs are read by developers who scan for one detail at a time — return type, fields, query params, defaults — and each gets its own sentence; P4 applied: metadata composition, pagination mechanism, and default value each occupy one sentence)*

>
> **Non-STE:** This framework provides a declarative approach to building REST APIs with automatic OpenAPI specification generation, built-in request validation against JSON schemas, and middleware for rate limiting, CORS handling, and structured request logging with configurable log levels and output formats. (39 words)
>
> **STE:** This framework gives a declarative approach to building REST APIs. It generates OpenAPI specifications automatically. It validates requests against JSON schemas. It includes middleware for rate limiting. It includes middleware for CORS handling. It includes middleware for request logging. You can configure log levels and output formats. (10, 5, 6, 6, 6, 6, 8 words)
>
> *(P3 applied: the 39-word README sentence is split into seven sentences, each 10 words or fewer; P1 applied: "provides" → "gives" uses an approved word and reduces word count; P4 applied: each framework feature — generation, validation, middleware types, configuration — gets its own sentence)*

## Principles Applied

**P3** — Keep sentences short and separate ideas. This is the primary principle for Rule 6.3. The 25-word maximum forces the writer to express one idea per sentence. Long sentences combine multiple ideas with coordinating conjunctions, relative clauses, and nested phrases. Short sentences isolate each idea so the reader can absorb one concept at a time. In code documentation, separating ideas into short sentences helps developers scan for the specific detail they need without parsing a dense multi-clause sentence.

**P4** — Write one topic per descriptive sentence. Short sentences are the enforcement mechanism for the one-topic-per-sentence rule. A sentence under 25 words can hold at most one descriptive fact about the code. When a sentence exceeds 25 words, it almost always mixes multiple topics — a function's purpose and its parameters, or an endpoint's return type and its query parameters. Splitting the sentence splits the topics. Each resulting sentence covers exactly one topic.

**P12** — Write for the target audience. Developers read code documentation by scanning for specific information. They look for a parameter name, a return type, an error condition, or an install command. When these details are packed into a single 40-word sentence, the developer must read the entire sentence to find one piece of information. Short sentences create natural scan points. A developer can find the return type because it has its own sentence. They can find the pagination default because it has its own sentence.

**P1** — Use approved words from the controlled terminology. Short sentences make non-approved vocabulary visible. Long sentences provide cover for verbose words like "utilize," "perform," "facilitate," and "implement." When each sentence is short, every word carries proportional weight. Jargon and non-approved words stand out and become obvious candidates for replacement. The discipline of short sentences naturally pushes the writer toward simpler, approved vocabulary.
