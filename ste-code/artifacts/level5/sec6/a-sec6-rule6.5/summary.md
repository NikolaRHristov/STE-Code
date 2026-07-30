# Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

## Original Rule Summary

Rule 6.5 requires that each paragraph in descriptive writing covers only one topic. The topic sentence is the first sentence in a paragraph and gives new information while making a logical connection to previous information, usually through a key word or connecting phrase. When a reader writes down the topic sentences from a text, those sentences form a good outline of the content. The other sentences in each paragraph give the information a logical structure and add more detail on the topic of the paragraph.

## STE-Code Adaptation

In code documentation, each paragraph must cover exactly one topic so that developers can scan topic sentences and build a mental outline of the documentation. README sections, API reference paragraphs, docstrings, commit message bodies, and changelog entries must each stay focused on one topic — do not mix installation with configuration, error handling with response format, or function purpose with side effects in the same paragraph. The topic sentence is the first sentence of a paragraph and contains a key term or connecting phrase that links the new topic to the previous paragraph. When a paragraph drifts into a second topic, split it at the topic boundary so the developer can find specific information by scanning only the first sentence of each paragraph.

## Example Pairs

> **Non-STE:** The `UserController` class handles all user-related API endpoints including registration, login, password reset, and profile management. To register a new user, send a POST request to `/api/users` with a JSON body containing `username`, `email`, and `password`. The controller validates the input against the `UserSchema` and stores a bcrypt hash of the password in the `users` table. The login endpoint at POST `/api/auth/login` accepts `email` and `password` and returns a JWT access token and a refresh token. The rate limiter allows 5 login attempts per minute per IP address to prevent brute force attacks, and failed attempts are logged to the `auth_audit` table for security monitoring.
>
> **STE:** The `UserController` class handles all user-related API endpoints. It manages registration, login, password reset, and profile management.
>
> To register a new user, send a POST request to `/api/users`. The request body must contain `username`, `email`, and `password` as a JSON object. The controller validates the input against the `UserSchema`. It stores a bcrypt hash of the password in the `users` table.
>
> To log in, send a POST request to `/api/auth/login`. The request body must contain `email` and `password`. The endpoint returns a JWT access token and a refresh token.
>
> The login endpoint uses a rate limiter. The rate limiter allows five login attempts per minute per IP address. Failed login attempts are logged to the `auth_audit` table for security monitoring.
>
> *(One paragraph blends registration, login, rate limiting, and audit logging. The STE version splits them into four paragraphs: controller overview, registration flow, login flow, and rate limiting.)*

>
> **Non-STE:** The `CacheManager` module provides a unified interface for caching data in either Redis or Memcached backends depending on the `CACHE_DRIVER` environment variable. It automatically serializes complex objects using MessagePack before storing them and handles TTL expiration by setting the `cache.ttl` configuration option to a value in seconds. The cache also supports tagging so you can group related cache entries under a shared tag and invalidate the entire group with a single `invalidateTag` call without knowing the individual keys ahead of time.

>
> **STE:** The `CacheManager` module gives a unified interface for caching data. It can use a Redis backend or a Memcached backend. Set the `CACHE_DRIVER` environment variable to choose the backend.
>
> The `CacheManager` serializes complex objects before storage. It uses the MessagePack format for serialization.
>
> The `CacheManager` supports time-to-live expiration. Set the `cache.ttl` configuration option to a value in seconds.
>
> The `CacheManager` supports cache tags. Group related cache entries under one tag. Use the `invalidateTag` method to invalidate all entries in the tag group. You do not need to know the individual keys.
>
> *(The Non-STE paragraph mixes serialization, TTL, and tagging. The STE version gives each topic its own paragraph: backend selection, serialization, TTL expiration, and tag-based invalidation.)*

>
> **Non-STE:** The `buildRelease` script compiles the application from source and runs the full test suite including unit integration and end-to-end tests against a staging database. It also minifies the frontend assets using Terser and CSSNano and calculates the SHA-256 checksum of the output binary which gets written to the `release/checksums.txt` manifest. After the build finishes the script uploads the artifacts to the S3 bucket defined in the `RELEASE_BUCKET` environment variable and creates a new GitHub release draft with the version number from `package.json`. Any failures during the build step cause the script to exit immediately with a non-zero code and write the error to `build-error.log` without attempting the upload step.

>
> **STE:** The `buildRelease` script compiles the application from source. It runs the full test suite against a staging database. The test suite includes unit tests, integration tests, and end-to-end tests.
>
> The `buildRelease` script minifies the frontend assets. It uses Terser for JavaScript files. It uses CSSNano for CSS files.
>
> The `buildRelease` script calculates the SHA-256 checksum of the output binary. It writes the checksum to the `release/checksums.txt` manifest.
>
> After the build is complete, the `buildRelease` script uploads the artifacts. It sends them to the S3 bucket defined in the `RELEASE_BUCKET` environment variable. It also creates a new GitHub release draft. The draft uses the version number from `package.json`.
>
> If the build fails, the `buildRelease` script exits with a non-zero code. It writes the error to the `build-error.log` file. It does not attempt the upload step.
>
> *(The Non-STE paragraph describes compilation, testing, minification, checksums, uploads, GitHub releases, and error handling in one paragraph. The STE version splits them into five paragraphs: build and test, asset minification, checksum generation, artifact upload, and error handling.)*

## Principles Applied

**P4** — Write one topic per descriptive sentence. This principle scales from the sentence level to the paragraph level. When each sentence addresses one subject, it is easier to see when a paragraph has drifted to a second topic. A paragraph with one topic naturally contains sentences that all relate to the same subject.

**P12** — Write for the target audience. Developers scan documentation by reading topic sentences. When each paragraph has exactly one topic, the developer can read only the first sentence of each paragraph and build an accurate outline. Mixed-topic paragraphs force the developer to read every sentence to find the information they need.

**P3** — Keep sentences short and separate ideas. One-topic paragraphs reinforce the short-sentence rule. When a paragraph covers multiple topics, the sentences tend to grow long with conjunctions and relative clauses to stitch the topics together. One-topic paragraphs remove that pressure — each sentence stays short because it only needs to add detail to a single topic.

**P2** — Use approved nouns from the dictionary. Consistent key terminology across paragraphs signals topic boundaries to the reader. When the same approved noun appears as the subject of consecutive topic sentences, the reader knows each paragraph handles a different aspect of the same concept. Changing terminology between paragraphs breaks this signal and makes the topic structure harder to follow.
