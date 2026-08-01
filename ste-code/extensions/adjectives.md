### idempotent

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes an operation that produces the same result when applied more than once, with no extra side effects after the first run.
- **code_example_ste**: Make the retry handler idempotent so a second call with the same input does not duplicate the record.
- **code_example_non_ste**: Leverage an idempotent retry handler so a duplicate invocation will not create a redundant record.
- **source**: generated-batch-002

### immutable

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a data structure or value that cannot be changed after it is created, which prevents accidental shared-state bugs.
- **code_example_ste**: Keep the request context immutable so concurrent threads cannot overwrite each other's values during a single operation.
- **code_example_non_ste**: Utilize an immutable request context so concurrent threads will not overwrite shared values during processing.
- **source**: generated-batch-002

### atomic

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes an operation that completes fully or not at all, with no partial result visible to other processes.
- **code_example_ste**: Wrap the balance update in an atomic transaction so the debit and credit always succeed or fail together.
- **code_example_non_ste**: Employ an atomic transaction to encapsulate the balance update so debit and credit always commit or roll back together.
- **source**: generated-batch-002

### thread-safe

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes code that functions correctly when accessed by multiple threads at the same time without external locking.
- **code_example_ste**: Mark the singleton constructor thread-safe so two threads can call it on first use without creating two instances.
- **code_example_non_ste**: Leverage a thread-safe singleton constructor so concurrent threads will not instantiate duplicate objects on first access.
- **source**: generated-batch-002

### asynchronous

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a call or task that starts and returns before its work finishes, so the caller can do other work meanwhile.
- **code_example_ste**: Make the file upload asynchronous so the user interface stays responsive while the transfer runs in the background.
- **code_example_non_ste**: Utilize an asynchronous upload mechanism so the user interface remains responsive while the transfer executes in the background.
- **source**: generated-batch-002

### concurrent

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes tasks that make progress within the same time period, interleaved by the scheduler rather than strictly sequentially.
- **code_example_ste**: Run the test suites in concurrent processes so the full check finishes in a fraction of the single-threaded time.
- **code_example_non_ste**: Employ concurrent processes to execute the test suites so the whole check terminates faster than a single-threaded run.
- **source**: generated-batch-002

### deterministic

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a function whose output depends only on its inputs, with no hidden state or time-based variation between runs.
- **code_example_ste**: Keep the hash function deterministic so the same key always maps to the same bucket across restarts.
- **code_example_non_ste**: Leverage a deterministic hash function so an identical key consistently maps to the same bucket after restarts.
- **source**: generated-batch-002

### deprecated

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes an API or feature that still works but that the maintainers plan to remove, so avoid new use of it.
- **code_example_ste**: Mark the old login endpoint deprecated and show a warning that points to the new token-based method.
- **code_example_non_ste**: Flag the legacy login endpoint as deprecated and utilize a warning that redirects callers to the token-based method.
- **source**: generated-batch-002

### nullable

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a field or variable that can hold a null value to indicate the absence of a meaningful value.
- **code_example_ste**: Make the middle-name field nullable so the profile save does not fail when the value is absent.
- **code_example_non_ste**: Configure the middle-name field as nullable so the profile persistence will not fail when the value is missing.
- **source**: generated-batch-002

### serializable

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes an object that can be converted to a byte stream and rebuilt elsewhere without losing its data.
- **code_example_ste**: Make the session object serializable so the cache layer can store it and restore it on the next request.
- **code_example_non_ste**: Utilize a serializable session object so the cache layer can persist and reconstitute it on the following request.
- **source**: generated-batch-002

### stateless

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a service that keeps no client data between requests, which makes horizontal scaling simpler and safer.
- **code_example_ste**: Build the authentication proxy stateless so any node can answer a request without shared session memory.
- **code_example_non_ste**: Employ a stateless authentication proxy so every node can service a request without shared session storage.
- **source**: generated-batch-002

### backward-compatible

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a change that older clients can still use without modification because the old interface still works.
- **code_example_ste**: Keep the API response backward-compatible so existing mobile apps keep working after the schema update.
- **code_example_non_ste**: Leverage a backward-compatible response format so legacy mobile clients remain functional after the schema update.
- **source**: generated-batch-002

### read-only

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a resource or mode that permits inspection but forbids any write, update, or delete operation.
- **code_example_ste**: Open the database handle read-only during reports so the query tool cannot change production data by mistake.
- **code_example_non_ste**: Utilize a read-only database handle for reports so the query tool cannot mutate production data accidentally.
- **source**: generated-batch-002

### recursive

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a function that calls itself with a smaller part of the problem until it reaches a base case.
- **code_example_ste**: Write the directory walker recursive so it visits every nested folder without a manual loop stack.
- **code_example_non_ste**: Employ a recursive directory walker so it traverses each nested folder without an explicit loop stack.
- **source**: generated-batch-002

### monotonic

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a counter or clock that only increases and never goes backward, which makes ordering safe.
- **code_example_ste**: Use a monotonic sequence for the event id so replays never create a lower number than a prior record.
- **code_example_non_ste**: Leverage a monotonic sequence for the event identifier so replays never yield a lower value than prior records.
- **source**: generated-batch-002

### transitive

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a permission or relation that flows through a chain, so a grant to a group reaches its members.
- **code_example_ste**: Make the role grant transitive so a user in a child team inherits the parent team's read access automatically.
- **code_example_non_ste**: Utilize a transitive role grant so a member of a child team inherits the parent team's read access automatically.
- **source**: generated-batch-002

### volatile

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a memory value that another thread or device can change at any time, so the compiler must reload it.
- **code_example_ste**: Declare the status flag volatile so the loop reads the hardware register again instead of using a cached copy.
- **code_example_non_ste**: Employ a volatile status flag so the loop reloads the hardware register rather than using a cached copy.
- **source**: generated-batch-002

### hierarchical

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes data or permissions arranged in parent-child levels where a child inherits settings from its ancestor.
- **code_example_ste**: Store the configuration in a hierarchical map so a child setting overrides only the matching branch of the tree.
- **code_example_non_ste**: Utilize a hierarchical configuration map so a child setting overrides solely the matching branch of the tree.
- **source**: generated-batch-002

### normalized

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a database schema arranged to remove redundant data and reduce update anomalies across tables.
- **code_example_ste**: Keep the user table normalized so the address lives in one row and every order references it by id.
- **code_example_non_ste**: Utilize a normalized user table so the address resides in one row and each order references it by identifier.
- **source**: generated-batch-002

### incremental

- **type**: adjective
- **approved**: true
- **replaces**:
- **definition**: Describes a build or update that processes only the changed parts instead of recomputing the whole result.
- **code_example_ste**: Run an incremental compile so the tool rebuilds only the modules whose source changed since the last run.
- **code_example_non_ste**: Employ an incremental compile so the tool reconstructs only the modules whose source changed since the prior run.
- **source**: generated-batch-002
