# Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.3

## Original Rule

Good technical writing uses short sentences for complex topics. Short sentences give a clear structure to your writing and make information easier to understand.

In descriptive writing, the maximum sentence length is 25 words. This is because descriptive text is more complex than procedural text.

## STE-Code Adaptation

Good code documentation uses short sentences for complex topics. Short sentences give a clear structure to your documentation and make information easier to understand.

In descriptive code documentation, the maximum sentence length is 25 words. This is because descriptive text is more complex than procedural text.

### Examples

> **STE:** The authentication middleware validates each incoming request before the controller processes it. (11 words)
>
> *Code-domain example — a short, single-subject sentence that respects the 25-word limit.*

> **Non-STE:** This function provides the ability to run arbitrary software applications within a sandboxed execution environment that isolates system resources. (21 words)
> **STE:** This function lets you run software applications in a sandbox. The sandbox isolates system resources. (8 words and 5 words)
>
> *Code-domain example — breaking one complex sentence into two shorter sentences improves clarity, even when the original is under 25 words.*

> **Non-STE:** The configuration loader reads the YAML manifest file from the filesystem and parses it into an in-memory representation that other modules can query at runtime to determine their operational parameters. (32 words)
> **STE:** The configuration loader reads the YAML manifest file from the filesystem. It parses the file into an in-memory representation. Other modules can query this representation at runtime. They use it to find their operational parameters. (20 words, 8 words, 7 words, and 8 words)
>
> *Code-domain example — a 32-word sentence is split into four sentences, each under the 25-word limit.*

> **Non-STE:** The cache invalidation strategy employs a time-to-live mechanism combined with a least-recently-used eviction policy to ensure that stale data is removed and memory consumption remains within the allocated heap budget. (34 words)
> **STE:** The cache invalidation strategy uses a time-to-live mechanism. It also uses a least-recently-used eviction policy. Together, these mechanisms remove stale data. They also keep memory consumption within the allocated heap budget. (16 words, 10 words, 7 words, and 10 words)
>
> *Code-domain example — a 34-word sentence is split into four sentences, each under the 25-word limit.*

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic
