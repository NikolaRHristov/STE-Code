# Rule 6.4 — Use Paragraphs to Show Related Information

## Original Rule Summary

Rule 6.4 requires that descriptive writing use paragraphs to group related information and give the text a logical sequence. Each paragraph must start with a topic sentence that tells the reader what the paragraph covers, followed by sentences that explain or expand on that topic. When a new paragraph starts, the reader knows that the text introduces a new topic or different information. This structure prevents walls of text and helps readers find specific information without reading everything.

## STE-Code Adaptation

In code documentation, Rule 6.4 requires each paragraph to group related information under a clear topic sentence so developers can scan for the section they need. A README paragraph that mixes installation steps with configuration options violates this rule — each topic must move to its own paragraph with its own topic sentence. API documentation, module docstrings, class descriptions, and architectural overviews must all break content into topic-focused paragraphs. When a new paragraph begins, the developer knows the documentation has moved to a new subject, and a quick scan of topic sentences reveals the document's overall structure.

## Example Pairs

> **Non-STE:** The data pipeline processes incoming events through a sequence of stages. Each stage transforms the event payload and passes it to the next stage. The first stage is validation, which checks the event schema and rejects malformed events. The second stage is enrichment, which adds metadata such as timestamps, source identifiers, and geolocation data from an external lookup service. The third stage is transformation, which converts the event into the target format required by downstream consumers such as the analytics warehouse and the real-time dashboard. The final stage is persistence, which writes the transformed event to the primary data store and to the event log for audit purposes. Error handling is implemented at each stage to catch exceptions without breaking the entire pipeline. If a stage fails, the pipeline logs the error and routes the event to the dead-letter queue for manual inspection.
>
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
> The second stage is enrichment. This stage adds metadata to the event. The metadata includes timestamps, source identifiers, and geolocation data from an external lookup service.
>
> **4. Transformation Stage**
>
> The third stage is transformation. This stage converts the event into the target format. Downstream consumers use this format. These consumers include the analytics warehouse and the real-time dashboard.
>
> **5. Persistence Stage**
>
> The final stage is persistence. This stage writes the transformed event to two destinations. It writes the event to the primary data store. It also writes the event to the event log for audit purposes.
>
> *(P4 applied: each stage occupies its own paragraph with a topic sentence that names the stage; P12 applied: a developer looking for the enrichment logic finds it instantly by scanning topic sentences for "enrichment"; P1 applied: topic sentences use approved vocabulary — "validates," "adds," "converts," "writes")*

>
> **Non-STE:** To install, run `pip install mylib` and then create a config file at `~/.mylib.toml` with your API key. The library supports Python 3.9 and above and requires a Redis instance for caching, which you can start with `redis-server`. You can also use SQLite for development without Redis.
>
> **STE:**
>
> **Installation**
>
> Install the library with pip. Run this command:
> ```
> pip install mylib
> ```
>
> **Configuration**
>
> Create a configuration file at `~/.mylib.toml`. Add your API key to this file.
>
> **Dependencies**
>
> The library supports Python 3.9 and above. A Redis instance is necessary for caching. Start Redis with this command: `redis-server`.
>
> For development without Redis, use SQLite as the cache backend.
>
> *(P4 applied: each paragraph covers one topic — installation, configuration, or dependencies; P12 applied: a developer scanning the README for "how to configure" finds the Configuration paragraph by its topic sentence; P3 applied: short sentences within each paragraph keep each topic clear)*

>
> **Non-STE:** The `GET /api/v1/orders/:id` endpoint retrieves a single order by its ID and requires a valid bearer token in the Authorization header, returning a 404 if the order is not found or a 403 if the user does not have permission to view the order. The response body is a JSON object with fields for the order ID, customer name, list of line items, total amount, and status, and the status field can be one of `pending`, `confirmed`, `shipped`, or `delivered`.
>
> **STE:**
>
> **Endpoint**
>
> The `GET /api/v1/orders/:id` endpoint retrieves a single order. Use the `:id` path parameter to identify the order.
>
> **Authentication**
>
> This endpoint requires a valid bearer token. Include the token in the `Authorization` header. If the token is missing or invalid, the endpoint returns a `401 Unauthorized` response. If the user does not have permission to view the order, the endpoint returns a `403 Forbidden` response.
>
> **Response**
>
> The endpoint returns a JSON object. The object contains these fields:
> - `id` — the order identifier
> - `customerName` — the name of the customer
> - `lineItems` — a list of items in the order
> - `total` — the total amount
> - `status` — the current status of the order.
>
> **Status Values**
>
> The `status` field can have one of these values: `pending`, `confirmed`, `shipped`, or `delivered`.
>
> **Error Responses**
>
> If the order is not found, the endpoint returns a `404 Not Found` response. The response body is an error object.
>
> *(P4 applied: five paragraphs — Endpoint, Authentication, Response, Status Values, Error Responses — each with its own topic sentence; P12 applied: a developer looking for error behavior finds it in the Error Responses paragraph immediately; P1 applied: topic sentences use approved words — "retrieves," "requires," "returns," "contains," "can have")*

## Principles Applied

**P4** — Write one topic per paragraph. This is the primary principle for Rule 6.4. Each paragraph must have exactly one topic, announced by its topic sentence at the start. When a paragraph mixes installation with configuration, or authentication with response format, the reader cannot scan for information efficiently. Topic sentences act as signposts that tell the developer what the paragraph covers. The sentences that follow must explain or expand on that topic only, not introduce a new topic that belongs in its own paragraph.

**P12** — Write for the target audience. Developers do not read documentation linearly. They scan for the specific section they need — authentication requirements, error codes, install commands. Topic-focused paragraphs with clear topic sentences make scanning fast and accurate. A developer looking for pagination details can skip every paragraph whose topic sentence does not mention pagination. This scanning behavior makes paragraph structure more important in code documentation than in general technical writing.

**P1** — Use approved words from the controlled terminology. Topic sentences must use the simplest approved words available. The topic sentence is the first thing a developer reads in each paragraph, so it must communicate the topic with zero ambiguity. Words like "utilizes," "facilitates," and "implements" obscure the topic — use "uses," "helps," and "does" instead. A topic sentence built from approved words tells the developer immediately what the paragraph covers.

**P3** — Write short sentences within each paragraph. Paragraph focus depends on sentence focus. If each sentence in a paragraph stays under 25 words and covers one idea, the paragraph as a whole stays on-topic. A paragraph with a 40-word sentence almost always drifts because that sentence tries to cover more than one subtopic. Short sentences keep each paragraph tight and prevent topic drift.

**P11** — Use approved technical names consistently across paragraphs. When a concept appears in multiple paragraphs, its name must stay the same every time. If the topic sentence of one paragraph says "the authentication middleware" and the topic sentence of the next paragraph says "the auth layer," the developer must pause to confirm these mean the same thing. Consistent technical naming across topic sentences makes the paragraph structure predictable and the document easier to scan.
