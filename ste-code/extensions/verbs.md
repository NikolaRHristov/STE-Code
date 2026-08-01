### use

- **type**: verb
- **category-id**: 1
- **approved**: true
- **replaces**: utilize, leverage, employ
- **definition**: Use a library or module to do a task. Do not use a more complex or vague word in code documentation.
- **code_example_ste**: Use the cache module to reduce the number of slow database queries during peak load.
- **code_example_non_ste**: Utilize the cache module to decrease the number of slow database queries during peak load.
- **source**: generated-batch-001

### start

- **type**: verb
- **category-id**: 15
- **approved**: true
- **replaces**: initiate, commence, bootstrap
- **definition**: Start a process, service, or background task so that it begins to run and accepts work from callers.
- **code_example_ste**: Start the worker process before the test suite sends its requests to the server.
- **code_example_non_ste**: Initiate the worker process before the test suite transmits its requests to the server.
- **source**: generated-batch-001

### stop

- **type**: verb
- **category-id**: 15
- **approved**: true
- **replaces**: terminate, halt, kill
- **definition**: Stop a running process, service, or timer so that it no longer runs and releases the resources it holds.
- **code_example_ste**: Stop the background job before you remove the temporary output directory from the disk.
- **code_example_non_ste**: Terminate the background job before you delete the temporary output directory from the disk.
- **source**: generated-batch-001

### show

- **type**: verb
- **category-id**: 9
- **approved**: true
- **replaces**: display, render, present
- **definition**: Show a value, message, or result to the user on the screen or in a log file for review.
- **code_example_ste**: Show the current configuration value in the terminal when the operator runs the status command now.
- **code_example_non_ste**: Display the present configuration value in the terminal when the operator runs the status command now.
- **source**: generated-batch-001

### make

- **type**: verb
- **category-id**: 6
- **approved**: true
- **replaces**: create, generate, produce
- **definition**: Make a new object, file, or connection in your code so that other functions can use it safely.
- **code_example_ste**: Make a new connection pool in the service constructor with the maximum size that you set.
- **code_example_non_ste**: Create a new connection pool in the service constructor with the maximum size that you set.
- **source**: generated-batch-001

### get

- **type**: verb
- **category-id**: 9
- **approved**: true
- **replaces**: retrieve, fetch, obtain
- **definition**: Get a value, record, or resource from a store or an API so that your code can use it.
- **code_example_ste**: Get the user record from the database with the identifier that the request provides.
- **code_example_non_ste**: Retrieve the user record from the database with the identifier that the request provides.
- **source**: generated-batch-001

### set

- **type**: verb
- **category-id**: 9
- **approved**: true
- **replaces**: configure, assign, establish
- **definition**: Set a value, property, or option on an object so that the program uses that value at runtime.
- **code_example_ste**: Set the timeout value on the client to five seconds before you send the first request.
- **code_example_non_ste**: Configure the timeout value on the client to five seconds before you send the first request.
- **source**: generated-batch-001

### check

- **type**: verb
- **category-id**: 15
- **approved**: true
- **replaces**: verify, validate, ensure
- **definition**: Check that a condition is true or that data is correct before your program continues to the next step.
- **code_example_ste**: Check that the input token is valid before the handler reads the protected user data.
- **code_example_non_ste**: Verify that the input token is valid before the handler reads the protected user data.
- **source**: generated-batch-001

### do

- **type**: verb
- **category-id**: 15
- **approved**: true
- **replaces**: perform, execute, carry out
- **definition**: Do an operation or a task in your code so that the program completes the work the user requested.
- **code_example_ste**: Do the cleanup step after the importer finishes reading the uploaded file.
- **code_example_non_ste**: Perform the cleanup step after the importer finishes reading the uploaded file.
- **source**: generated-batch-001

### send

- **type**: verb
- **category-id**: 3
- **approved**: true
- **replaces**: transmit, dispatch, forward
- **definition**: Send a message, request, or event from one component to another so that the receiver can act on it.
- **code_example_ste**: Send the error event to the logger so that the operator can see the failure in the dashboard.
- **code_example_non_ste**: Transmit the error event to the logger so that the operator can see the failure in the dashboard.
- **source**: generated-batch-001

### remove

- **type**: verb
- **category-id**: 9
- **approved**: true
- **replaces**: delete, eliminate, purge
- **definition**: Remove an item, file, or entry from a collection or a store so that it is no longer available to callers.
- **code_example_ste**: Remove the stale cache entry when the write operation finishes and the data changes.
- **code_example_non_ste**: Delete the stale cache entry when the write operation finishes and the data changes.
- **source**: generated-batch-001

### keep

- **type**: verb
- **category-id**: 9
- **approved**: true
- **replaces**: retain, preserve, maintain
- **definition**: Keep a value, file, or connection so that your program can use it again in a later step without rework.
- **code_example_ste**: Keep the open socket so that the next request does not pay the cost of a new connection.
- **code_example_non_ste**: Retain the open socket so that the next request does not pay the cost of a new connection.
- **source**: generated-batch-001

### leverage

- **type**: verb
- **category-id**: 1
- **approved**: false
- **replaces**:
- **definition**: A rejected synonym for "use". Avoid this jargon word in code documentation and write "use" instead for clear instructions.
- **code_example_ste**: Use the cache layer to reduce the load on the primary database during peak traffic.
- **code_example_non_ste**: Leverage the cache layer to reduce the load on the primary database during peak traffic.
- **source**: generated-batch-001

### utilize

- **type**: verb
- **category-id**: 1
- **approved**: false
- **replaces**:
- **definition**: A rejected synonym for "use". Do not write this word in code documentation. Write "use" to give a clear instruction.
- **code_example_ste**: Use the logging library to record the start and the end of each request.
- **code_example_non_ste**: Utilize the logging library to record the start and the end of each request.
- **source**: generated-batch-001

### commence

- **type**: verb
- **category-id**: 15
- **approved**: false
- **replaces**:
- **definition**: A rejected synonym for "start". Do not use this word in code documentation. Write "start" to give a clear and direct instruction.
- **code_example_ste**: Start the migration script before the application accepts traffic from clients.
- **code_example_non_ste**: Commence the migration script before the application accepts traffic from clients.
- **source**: generated-batch-001

### terminate

- **type**: verb
- **category-id**: 15
- **approved**: false
- **replaces**:
- **definition**: A rejected synonym for "stop". Avoid this word in code documentation. Write "stop" so that the instruction is short and clear.
- **code_example_ste**: Stop the server process after the integration tests complete and write their results.
- **code_example_non_ste**: Terminate the server process after the integration tests complete and write their results.
- **source**: generated-batch-001

### display

- **type**: verb
- **category-id**: 9
- **approved**: false
- **replaces**:
- **definition**: A rejected synonym for "show". Do not write this word in code documentation. Write "show" to keep the instruction simple.
- **code_example_ste**: Show the error count in the status panel so the operator can see the failed jobs.
- **code_example_non_ste**: Display the error count in the status panel so the operator can see the failed jobs.
- **source**: generated-batch-001

### employ

- **type**: verb
- **category-id**: 1
- **approved**: false
- **replaces**:
- **definition**: A rejected synonym for "use". Do not use this word in code documentation. Write "use" to make the instruction direct and easy to read.
- **code_example_ste**: Use the retry helper to handle the transient network errors in the client code.
- **code_example_non_ste**: Employ the retry helper to handle the transient network errors in the client code.
- **source**: generated-batch-001

### render

- **type**: verb
- **category-id**: 9
- **approved**: false
- **replaces**:
- **definition**: A rejected synonym for "show". Avoid this word in code documentation. Write "show" so that the instruction is clear to every reader.
- **code_example_ste**: Show the loading indicator while the page fetches the list of available reports.
- **code_example_non_ste**: Render the loading indicator while the page fetches the list of available reports.
- **source**: generated-batch-001

### validate

- **type**: verb
- **category-id**: 15
- **approved**: false
- **replaces**:
- **definition**: A rejected synonym for "check". Do not write this word in code documentation. Write "check" to keep the instruction short and clear.
- **code_example_ste**: Check that the configuration file is valid before the server starts to accept connections.
- **code_example_non_ste**: Validate that the configuration file is valid before the server starts to accept connections.
- **source**: generated-batch-001
