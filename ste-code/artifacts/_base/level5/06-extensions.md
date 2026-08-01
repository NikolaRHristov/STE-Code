## Extensions

# Extension adjectives

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
- **code_example_ste**: Run the test suites in concurrent processes so the full check finishes in a fraction of the
