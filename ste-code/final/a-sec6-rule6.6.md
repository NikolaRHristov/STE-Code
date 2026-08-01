# Rule 6.6 — Make Sure That No Paragraph Has More Than Six Sentences

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 6.6

> **Source:** [master.md#sec6-rule6.6](ste-code/grouped/)

> Source: master.md#sec6-rule6.6

## Original Rule

Make sure that no paragraph has more than six sentences. Paragraphs divide a text into logical units and help keep the reader's attention. If paragraphs are too long, they cannot have this function. Do not put different topics in the same paragraph. If a paragraph has more than six sentences, divide it into two smaller paragraphs. This structure will make your text easier to read.

## STE-Code Adaptation

In code documentation, make sure that no paragraph has more than six sentences. Paragraphs divide a documentation block into logical units and help keep the developer's attention. If paragraphs are too long, they cannot have this function. Do not put different topics in the same paragraph. If a paragraph has more than six sentences, divide it into two smaller paragraphs. This structure will make your documentation easier to read.

### Examples

> **Non-STE:** The connection pool manager (1) has these primary components: a set of pre-allocated socket connections that the manager reuses across requests to avoid the cost of repeated TCP handshakes and TLS negotiation, a background reaper thread that closes connections that have been idle longer than the idle timeout and that also runs a periodic health probe to detect dropped links, a bounded queue that holds pending acquire requests when all connections are in use and that rejects new requests with a timeout error after the acquire timeout expires, and a metrics collector that records the number of active connections, the wait time distribution, and the count of rejected acquires for the observability stack; together these parts let the application serve high request rates without opening a new connection for every call. (5 sentences, but each is very long and dense)
>
> **STE:** The connection pool manager (1) has these primary parts:
> - A set of pre-allocated socket connections that the manager reuses across requests.
> - A background reaper thread.
> - A bounded queue for pending acquire requests.
> - A metrics collector.
>
> The socket connections let the application reuse one link for many requests. The reuse avoids repeated TCP handshakes and TLS negotiation.
>
> The reaper thread closes connections that are idle longer than the idle timeout. The reaper thread also runs a periodic health probe to find dropped links.
>
> The bounded queue holds pending acquire requests when all connections are in use. The queue rejects new requests with a timeout error after the acquire timeout expires.
>
> The metrics collector records the number of active connections. The collector also records the wait time distribution and the count of rejected acquires. The observability stack reads these metrics.
>
> *Code-domain example — the Non-STE version puts four unrelated components and their behaviors into one paragraph of five overlong sentences. The STE version splits the description into one short outline paragraph and four short paragraphs, each with its own topic and fewer than six sentences.*

> **Non-STE:** The request handler module accepts an HTTP request, parses the JSON body, validates the schema against the openapi specification, authenticates the caller with the OAuth provider, authorizes the action against the role table, loads the target record from the primary database, applies the business rules, writes the audit entry, commits the transaction, and returns a 200 response with the updated resource, and if any step fails it rolls back the transaction and returns the appropriate 4xx or 5xx status with an error body. (1 sentence, 1 paragraph — far too much for one paragraph)
>
> **STE:** The request handler module accepts an HTTP request. It parses the JSON body of the request.
>
> The handler validates the request schema against the openapi specification. It authenticates the caller with the OAuth provider. The handler authorizes the action against the role table.
>
> The handler loads the target record from the primary database. It applies the business rules to the record. The handler writes an audit entry. It commits the transaction. The handler returns a 200 response with the updated resource.
>
> If any step fails, the handler rolls back the transaction. It returns the appropriate 4xx or 5xx status with an error body.
>
> *Code-domain example — the Non-STE version crams an entire request lifecycle into a single one-paragraph sentence. The STE version breaks the lifecycle into four paragraphs of two to four sentences each, one paragraph per phase: parse, authorize, act, and fail.*

## Code-Domain Explanation

This rule keeps documentation readable by limiting the size of each paragraph. A paragraph is a group of sentences that share one topic. When a paragraph grows past six sentences, the reader loses the thread of the topic and must re-read to recover the structure. The six-sentence limit is a practical ceiling, not a target. Most good paragraphs use two to four sentences.

Rule 6.6 works with Rule 6.4 (use paragraphs to show related information) and Rule 6.5 (each paragraph has only one topic). Rule 6.4 tells you to use paragraphs. Rule 6.5 tells you to give each paragraph one topic. Rule 6.6 tells you not to let a paragraph grow past six sentences. The three rules together produce short, single-topic paragraphs that the developer can scan quickly.

### When to split a paragraph

Split a paragraph when any of these conditions is true:

- The paragraph has more than six sentences.
- The paragraph covers two or more topics (see Rule 6.5).
- A sentence in the paragraph introduces a new key word that the earlier sentences do not use (see Rule 6.2).

When you split, put the sentences that share one key word in the first paragraph. Put the sentences that share a different key word in the second paragraph. Start the second paragraph with a topic sentence that names the new key word.

### README Files

In a README, keep each feature description to a short paragraph. A feature paragraph that lists installation, configuration, and usage in one block of eight sentences forces the reader to parse three topics at once. Split it: one paragraph for what the feature does, one paragraph for how to enable it, one paragraph for a usage example.

### API Documentation

In API documentation, keep each endpoint description in a short paragraph. Do not describe the request format, the authentication requirement, the response shape, and the error conditions in one long paragraph. Use one paragraph for the purpose of the endpoint, one paragraph for the request, one paragraph for the response, and one paragraph for the errors. Each paragraph must stay under six sentences.

### Docstrings

In a docstring, keep the summary paragraph short. If the docstring explains the parameters, the return value, and the raised exceptions, use one short paragraph per concern. A docstring that lists every parameter and every exception in one six-sentence paragraph is acceptable only if all the sentences describe the same function. If the parameter list grows long, move it to a bulleted list (as shown in the Examples) and keep the prose paragraph under six sentences.

### Error Messages and Log Entries

An error message is usually one sentence. A log entry is usually one line. These rarely reach six sentences. The rule applies when you write a recovery note or a multi-line diagnostic block. Keep the diagnostic block to six lines or fewer, or split it into a cause paragraph and a recovery paragraph.

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

In object-oriented documentation, describe one responsibility per paragraph. When you document a class with several collaborators, give each collaborator its own short paragraph.

> **Non-STE:** The `OrderService` class creates orders, validates the cart total against the pricing service, reserves inventory through the warehouse client, charges the payment gateway, sends a confirmation email via the notification service, writes the order to the orders table, and emits an `OrderCreated` event to the message bus, and it also handles the compensation flow that releases inventory and refunds the payment if the downstream confirmation fails.
>
> **STE:** The `OrderService` class creates orders. It validates the cart total with the pricing service.
>
> The `OrderService` reserves inventory through the warehouse client. It charges the payment gateway.
>
> The `OrderService` sends a confirmation email via the notification service. It writes the order to the `orders` table. The class emits an `OrderCreated` event to the message bus.
>
> If the downstream confirmation fails, the `OrderService` runs a compensation flow. The flow releases the reserved inventory. The flow also refunds the payment.
>
> *Principles applied: P5, P11 — each paragraph covers one phase of the order lifecycle and stays under six sentences.*

### Functional (Haskell, Elixir, Clojure, Rust)

In functional documentation, describe one transformation stage per paragraph. A pipeline that maps, filters, and folds should not live in one paragraph.

> **Non-STE:** The `compile` function parses the source string into a token stream, builds an abstract syntax tree, runs the type checker to infer and unify types, applies the desugaring pass that removes syntactic sugar, optimizes the tree with constant folding and dead code elimination, and finally emits the target bytecode, logging each stage to the compiler trace for debugging.
>
> **STE:** The `compile` function parses the source string into a token stream. It builds an abstract syntax tree from the tokens.
>
> The function runs the type checker. The checker infers and unifies the types.
>
> The function applies the desugaring pass. The pass removes syntactic sugar.
>
> The function optimizes the tree. The optimization uses constant folding and dead code elimination.
>
> The function emits the target bytecode. It logs each stage to the compiler trace.
>
> *Principles applied: P2, P10 — each pipeline stage is its own paragraph with fewer than six sentences.*

### Procedural (C, Go, Bash)

In procedural documentation, describe one phase of the script per paragraph. Do not document setup, execution, and cleanup in one paragraph.

> **Non-STE:** The `deploy.sh` script reads the target environment from the first argument, loads the secrets from the vault into environment variables, builds the container image with the build tag, pushes the image to the registry, updates the manifest in the cluster, waits for the rollout to complete, runs a smoke test against the health endpoint, and sends a notification to the release channel, and if the smoke test fails it rolls back the manifest and alerts the on-call engineer.
>
> **STE:** The `deploy.sh` script reads the target environment from the first argument. It loads the secrets from the vault into environment variables.
>
> The script builds the container image with the build tag. It pushes the image to the registry.
>
> The script updates the manifest in the cluster. It waits for the rollout to complete.
>
> The script runs a smoke test against the health endpoint. It sends a notification to the release channel.
>
> If the smoke test fails, the script rolls back the manifest. It alerts the on-call engineer.
>
> *Principles applied: P7, P10 — the build, rollout, verify, and fail phases are separate paragraphs, each under six sentences.*

### Declarative (SQL, Terraform, Kubernetes YAML)

In declarative documentation, describe one resource or one block per paragraph. A module that declares a database, a cache, and a queue should document each in its own paragraph.

> **Non-STE:** The `web_app` module provisions a PostgreSQL instance with automated backups and a read replica, a Redis cache with a fixed eviction policy, an S3 bucket for static assets with lifecycle rules that expire old objects, a load balancer that distributes traffic across the instances, and a CloudWatch alarm that pages on high CPU, and the module wires the security groups so that only the app tier can reach the database and only the load balancer can reach the app tier.
>
> **STE:** The `web_app` module provisions a PostgreSQL instance. The instance uses automated backups. It also uses a read replica.
>
> The module provisions a Redis cache. The cache uses a fixed eviction policy.
>
> The module provisions an S3 bucket for static assets. The bucket uses lifecycle rules that expire old objects.
>
> The module provisions a load balancer. The load balancer distributes traffic across the instances.
>
> The module provisions a CloudWatch alarm. The alarm pages on high CPU.
>
> The module wires the security groups. Only the app tier can reach the database. Only the load balancer can reach the app tier.
>
> *Principles applied: P5, P11 — each resource is its own paragraph; the security group paragraph is the sixth and final paragraph, still under the limit.*

### Systems (Rust Ownership, C Memory)

In systems documentation, describe one ownership rule per paragraph. Memory contracts are easy to bury in a long paragraph. Keep each contract to a few sentences.

> **Non-STE:** The `Buffer` type owns a heap allocation that it frees on drop, it hands out borrowed slices through the `as_slice` method that tie their lifetime to the `Buffer`, it supports a `split_at` method that returns two non-overlapping borrowed slices for parallel processing, it clones cheaply by reference counting the underlying allocation when the `Arc` backend is selected, and it panics if a caller holds a borrowed slice and then calls a method that would reallocate the underlying buffer, because that would invalidate the borrowed slice.
>
> **STE:** The `Buffer` type owns a heap allocation. It frees the allocation on drop.
>
> The `Buffer` hands out borrowed slices through the `as_slice` method. The slice lifetime ties to the `Buffer`.
>
> The `Buffer` supports a `split_at` method. The method returns two non-overlapping borrowed slices for parallel processing.
>
> The `Buffer` clones cheaply when the `Arc` backend is selected. The clone reference counts the underlying allocation.
>
> The `Buffer` panics if a caller holds a borrowed slice and then calls a method that reallocates. The reallocation would invalidate the borrowed slice.
>
> *Principles applied: P7, P11 — each ownership rule is its own paragraph; the panic rule is the fifth paragraph, under the six-sentence limit.*

## Extended Examples

### Example 1: Module Overview That Stays Under the Limit

> **Non-STE:** The `AuthModule` provides login, logout, token refresh, and password reset, it integrates with the OAuth provider for social login and with the email service for reset links, it stores sessions in the Redis cache with a configurable TTL and replicates them across regions for availability, it enforces rate limits on the login endpoint to block credential stuffing attacks, and it emits security events to the audit log for every privileged action, and the module exposes a health check that reports the status of the OAuth provider, the Redis cache, and the email service so that the orchestrator can remove an unhealthy instance from the pool.
>
> **STE:** The `AuthModule` provides login, logout, token refresh, and password reset.
>
> The `AuthModule` integrates with the OAuth provider for social login. It also integrates with the email service for reset links.
>
> The `AuthModule` stores sessions in the Redis cache. The sessions use a configurable TTL. The module replicates sessions across regions for availability.
>
> The `AuthModule` enforces rate limits on the login endpoint. The limits block credential stuffing attacks.
>
> The `AuthModule` emits security events to the audit log for every privileged action.
>
> The `AuthModule` exposes a health check. The check reports the status of the OAuth provider, the Redis cache, and the email service. The orchestrator removes an unhealthy instance from the pool.
>
> *Principles applied: P6, P11 — six paragraphs, each under six sentences, one topic per paragraph.*

### Example 2: A Long Paragraph That Must Be Split

> **Non-STE:** The migration adds a `tenant_id` column to the `invoices` table, backfills the column from the `accounts` table using the account-to-tenant mapping, creates a partial index on `tenant_id` where the row is active, updates the `InvoiceRepository` query methods to filter by the current tenant, adds a foreign key from `invoices.tenant_id` to `tenants.id`, enables row-level security on the `invoices` table with a policy that matches the session tenant, and rewrites the reporting queries to aggregate per tenant instead of globally, and the migration runs online with concurrent index creation so that the `invoices` table stays available during the backfill. (1 paragraph, 1 sentence — violates Rule 6.6 because the single sentence describes seven distinct changes)
>
> **STE:** The migration adds a `tenant_id` column to the `invoices` table. It backfills the column from the `accounts` table.
>
> The migration creates a partial index on `tenant_id` for active rows. It adds a foreign key from `invoices.tenant_id` to `tenants.id`.
>
> The migration updates the `InvoiceRepository` query methods. The methods now filter by the current tenant.
>
> The migration enables row-level security on the `invoices` table. The policy matches the session tenant.
>
> The migration rewrites the reporting queries. The queries now aggregate per tenant instead of globally.
>
> The migration runs online with concurrent index creation. The `invoices` table stays available during the backfill.
>
> *Principles applied: P10, P12 — the seven changes become six short paragraphs, each under six sentences, instead of one unreadable paragraph.*

### Example 3: Configuration Reference With a Bulleted Paragraph

> **Non-STE:** The `server` section of the configuration file has these settings: `host` sets the bind address and defaults to `0.0.0.0`, `port` sets the listen port and defaults to `8080`, `max_connections` caps the concurrent client connections and defaults to `1024`, `read_timeout` sets the time to wait for a request and defaults to `30s`, `tls.cert` points to the certificate file and `tls.key` points to the private key file, and `keepalive` sets the idle connection timeout and defaults to `60s`, and all of these settings can be overridden by environment variables with the same name prefixed by `SERVER_`. (1 paragraph, 1 sentence — too dense)
>
> **STE:** The `server` section of the configuration file has these settings:
> - `host` — the bind address. The default is `0.0.0.0`.
> - `port` — the listen port. The default is `8080`.
> - `max_connections` — the cap on concurrent client connections. The default is `1024`.
> - `read_timeout` — the time to wait for a request. The default is `30s`.
> - `tls.cert` — the path to the certificate file.
> - `tls.key` — the path to the private key file.
> - `keepalive` — the idle connection timeout. The default is `60s`.
>
> You can override all of these settings with environment variables. Use the same name with the `SERVER_` prefix.
>
> *Principles applied: P9 — the long list becomes a bulleted paragraph for the settings and one short prose paragraph for the override rule, keeping the prose under six sentences.*

### Example 4: Changelog Entry That Respects the Limit

> **Non-STE:** The v3.1.0 release adds a streaming export mode for the report builder that yields rows to the client as they are computed instead of buffering the whole result, deprecates the `exportCsv` synchronous method in favor of the new `streamExport` method, fixes a bug where the date filter ignored the timezone of the report viewer and returned rows from the wrong day, improves the dashboard load time by deferring the loading of the secondary widgets until the primary chart renders, and updates the dependency on the charting library to a version that patches a cross-site scripting vulnerability in the tooltip renderer.
>
> **STE:** The v3.1.0 release has these changes:
>
> BREAKING: The `exportCsv` synchronous method is deprecated. Use the new `streamExport` method instead.
>
> Add a streaming export mode for the report builder. The mode yields rows to the client as they are computed. It does not buffer the whole result.
>
> Fix a bug in the date filter. The filter ignored the timezone of the report viewer. It returned rows from the wrong day.
>
> Improve the dashboard load time. Defer the loading of the secondary widgets until the primary chart renders.
>
> Update the charting library dependency. The new version patches a cross-site scripting vulnerability in the tooltip renderer.
>
> *Principles applied: P11 — each change type is its own short paragraph; the deprecation uses the DEPRECATED mapping through BREAKING for an API removal.*

### Example 5: Test Plan Description With Separate Paragraphs

> **Non-STE:** The integration test suite sets up a temporary database, seeds it with fixture data for three users and two tenants, starts the application in a background process bound to a test port, waits for the health check to report ready, runs the happy-path scenario that creates an order and verifies the invoice, runs the failure scenario that simulates a payment gateway timeout and verifies the compensation flow, runs the concurrency scenario that issues one hundred parallel requests and verifies that no two responses share a sequence number, tears down the application process, and drops the temporary database, and the suite writes a JUnit report to the `build/reports` directory and exits with a non-zero status if any scenario fails.
>
> **STE:** The integration test suite sets up a temporary database. It seeds the database with fixture data for three users and two tenants.
>
> The suite starts the application in a background process. The process binds to a test port. The suite waits for the health check to report ready.
>
> The suite runs the happy-path scenario. The scenario creates an order and verifies the invoice.
>
> The suite runs the failure scenario. The scenario simulates a payment gateway timeout. It verifies the compensation flow.
>
> The suite runs the concurrency scenario. The scenario issues one hundred parallel requests. It verifies that no two responses share a sequence number.
>
> The suite tears down the application process. It drops the temporary database. The suite writes a JUnit report to the `build/reports` directory. It exits with a non-zero status if any scenario fails.
>
> *Principles applied: P10, P12 — the setup, run, and teardown phases are separate paragraphs, each under six sentences.*

## Edge Cases

### Edge Case 1: A Paragraph That Needs More Than Six Sentences for One Topic

Some topics are intrinsically complex and need more than six sentences to explain one idea. In that case, keep the paragraph under six sentences and continue the same topic in a second paragraph. Start the second paragraph with a connecting phrase such as "Also," or "In addition," so the reader knows the topic continues.

> **Non-STE:** The garbage collector traces live objects, marks them, sweeps the unreachable ones, compacts the heap to reduce fragmentation, and records the pause time to the metrics endpoint, and it also promotes long-lived objects to the old generation, adjusts the survivor space ratio based on the observed promotion rate, and logs a concurrent mode failure when the heap fills faster than it can reclaim, which forces a full stop-the-world collection that the latency budget must absorb.
>
> **STE:** The garbage collector traces live objects. It marks them. It sweeps the unreachable objects. It compacts the heap to reduce fragmentation. It records the pause time to the metrics endpoint.
>
> In addition, the collector promotes long-lived objects to the old generation. It adjusts the survivor space ratio from the promotion rate. It logs a concurrent mode failure when the heap fills faster than it can reclaim. The failure forces a full stop-the-world collection. The latency budget must absorb that collection.
>
> *Principles applied: P6, P10 — the topic (garbage collection) continues across two paragraphs, each under six sentences.*

### Edge Case 2: A List Paragraph Counts as One Paragraph

A bulleted or numbered list is one paragraph, regardless of how many items it contains. Rule 6.6 limits the prose sentences that surround or introduce the list, not the number of list items. Keep the introductory sentence short. Do not add a long closing sentence that restates every item.

> **Non-STE:** The deployment manifest must include all of the following resources, and you should verify each one before you apply the manifest because a missing resource will cause the rollout to fail and the orchestrator will not roll back automatically so you will need to inspect the events and apply the correction by hand: the config map, the secret, the deployment, the service, the ingress, the horizontal pod autoscaler, the pod disruption budget, and the network policy.
>
> **STE:** The deployment manifest must include these resources:
> - The config map.
> - The secret.
> - The deployment.
> - The service.
> - The ingress.
> - The horizontal pod autoscaler.
> - The pod disruption budget.
> - The network policy.
>
> Verify each resource before you apply the manifest. A missing resource causes the rollout to fail.
>
> *Principles applied: P9 — the list is one paragraph; the surrounding prose stays under six sentences.*

### Edge Case 3: Generated Documentation That Produces Long Paragraphs

Auto-generated reference docs (from JSDoc, Sphinx, or OpenAPI generators) often emit one long paragraph per symbol. You cannot always control the generator output. When you can, set the generator to break the description at sentence boundaries. When you cannot, add a short human-written summary above the generated block. The summary must follow Rule 6.6. The generated block is exempt only if you do not edit its source annotations.

### Edge Case 4: A Paragraph That Mixes Two Topics but Stays Under Six Sentences

A short paragraph can still violate Rule 6.5 by mixing two topics. Rule 6.6 and Rule 6.5 are independent. A three-sentence paragraph that describes both the cache and the queue in unrelated ways must split even though it is under the sentence limit.

> **Non-STE:** The cache stores the rendered pages. The queue buffers the email jobs. The cache uses a least-recently-used eviction policy.
>
> **STE:** The cache stores the rendered pages. It uses a least-recently-used eviction policy.
>
> The queue buffers the email jobs.
>
> *Principles applied: P11 — the cache and the queue are two topics; split them even though the original is only three sentences.*

## Cross-References

- **Rule 6.4 — Use Paragraphs to Show Related Information:** Rule 6.6 is the size limit that Rule 6.4 assumes. Use paragraphs to group related information, then keep each paragraph under six sentences.
- **Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic:** Rule 6.6 limits the sentence count; Rule 6.5 limits the topic count. A paragraph can be short and still wrong if it mixes topics. Check both rules.
- **Rule 6.1 — Give Information Gradually:** Short paragraphs support gradual information delivery. When you split a long paragraph, the new paragraphs continue the same flow sentence by sentence.
- **Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure:** The key word of a paragraph is the topic. When you split a paragraph, the new paragraph starts with the new key word as its topic sentence.
- **Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence:** Short sentences make it easier to stay under six sentences per paragraph. A paragraph of six short sentences reads faster than a paragraph of three long sentences.

## Grammar Notes

### Why six sentences

The six-sentence limit comes from reading psychology. A reader holds the topic of a paragraph in working memory. After about six sentences, the topic fades and the reader must re-read to recover it. The limit is a guard against paragraph drift, where the writer adds one more sentence and the paragraph quietly changes topic.

### Sentence count, not word count

Rule 6.6 counts sentences, not words. A paragraph can have six short sentences or six long sentences and still pass the rule. However, a paragraph of six long sentences is harder to read than a paragraph of six short sentences. Apply Rule 6.3 (maximum 25 words per sentence) together with Rule 6.6 for the best result. A paragraph of six sentences that each have 25 words is at the edge of readability. Prefer two to four sentences per paragraph.

### Lists and tables reset the count

A bulleted list, a numbered list, or a table inside a paragraph does not add to the sentence count of the surrounding prose. The introductory sentence and the closing sentence are the prose. Keep those under six sentences total. If the list needs explanation, put the explanation in the list items, not in a long closing sentence.

### Splitting technique

When a paragraph exceeds six sentences, split at the sentence where the key word changes (see Rule 6.2) or where the topic changes (see Rule 6.5). Put the first group of sentences in the original paragraph. Start a new paragraph with a topic sentence that names the new key word. Do not repeat the old key word in the new paragraph unless it is part of the new topic.

### Interaction with procedures

In procedural writing (Section 5), each step is its own paragraph by convention. Rule 6.6 rarely applies to procedures because steps are short. It applies when a step description includes a long note or rationale. Keep the note under six sentences or move it to a separate note paragraph.
