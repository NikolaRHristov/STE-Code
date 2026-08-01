### AP-001

- **id**: AP-001
- **type**: anti-pattern
- **pattern**: Future tense in procedural instructions
- **non_ste**: The system will send a confirmation email after the registration process completes successfully.
- **ste**: The system sends a confirmation email after registration completes.
- **violates**: [P2, P4]
- **severity**: error
- **context**: User-facing documentation, onboarding guides, API tutorials

### AP-002

- **id**: AP-002
- **type**: anti-pattern
- **pattern**: Undefined acronym in error message
- **non_ste**: Error: DAG execution failed at T2.
- **ste**: Error: The scheduled workflow (DAG) failed at step T2. Open the dashboard to see the step log.
- **violates**: [P1, P8]
- **severity**: blocking
- **context**: CLI error messages, log output, alert notifications

### AP-003

- **id**: AP-003
- **type**: anti-pattern
- **pattern**: Passive voice obscures the actor
- **non_ste**: The configuration file is read by the service at startup and is validated before the connection is established.
- **ste**: The service reads the configuration file at startup. The service validates the file before it establishes the connection.
- **violates**: [P1, P3]
- **severity**: blocking
- **context**: API reference documentation, service configuration guides

### AP-004

- **id**: AP-004
- **type**: anti-pattern
- **pattern**: Nominalization instead of a direct verb
- **non_ste**: Perform the installation of the package and execute the initialization of the database before you commence the server.
- **ste**: Install the package and initialize the database before you start the server.
- **violates**: [P1, P4]
- **severity**: error
- **context**: Setup guides, installation README files

### AP-005

- **id**: AP-005
- **type**: anti-pattern
- **pattern**: Avoided synonym "utilize" for "use"
- **non_ste**: Utilize the cache layer to reduce database load during peak traffic periods.
- **ste**: Use the cache layer to reduce database load during peak traffic.
- **violates**: [P1]
- **severity**: error
- **context**: Developer guides, performance tuning docs

### AP-006

- **id**: AP-006
- **type**: anti-pattern
- **pattern**: Overlong sentence with nested clauses
- **non_ste**: When the user submits the form which contains invalid data the application will display an error message and it will also log the failure so that the team can investigate the root cause later.
- **ste**: When the user submits a form with invalid data, the application shows an error message. The application also logs the failure so the team can investigate.
- **violates**: [P4, P2]
- **severity**: warning
- **context**: User-facing error documentation, form validation guides

### AP-007

- **id**: AP-007
- **type**: anti-pattern
- **pattern**: Contraction in procedural documentation
- **non_ste**: Don't close the socket until the response isn't fully received.
- **ste**: Do not close the socket until the response is fully received.
- **violates**: [P1]
- **severity**: error
- **context**: Network programming guides, API documentation

### AP-008

- **id**: AP-008
- **type**: anti-pattern
- **pattern**: Jargon without definition
- **non_ste**: The ingress controller reconciles the desired state with the cluster and emits events on drift.
- **ste**: The ingress controller matches the cluster state to the configuration that you specify. It reports an event when the states differ.
- **violates**: [P1, P8]
- **severity**: error
- **context**: Infrastructure documentation, Kubernetes guides

### AP-009

- **id**: AP-009
- **type**: anti-pattern
- **pattern**: Semicolon joining two independent instructions
- **non_ste**: Open the settings file; then change the port value to 8080.
- **ste**: Open the settings file. Change the port value to 8080.
- **violates**: [P1]
- **severity**: error
- **context**: Configuration tutorials, step-by-step guides

### AP-010

- **id**: AP-010
- **type**: anti-pattern
- **pattern**: Avoided synonym "leverage" for "use"
- **non_ste**: Leverage the retry queue to handle transient failures without dropping requests.
- **ste**: Use the retry queue to handle transient failures without dropping requests.
- **violates**: [P1]
- **severity**: error
- **context**: Resilience documentation, failure-handling guides

### AP-011

- **id**: AP-011
- **type**: anti-pattern
- **pattern**: Ambiguous pronoun reference
- **non_ste**: The client calls the server and it returns the token, then it validates it before it stores it in memory.
- **ste**: The client calls the server. The server returns the token. The client validates the token and then stores it in memory.
- **violates**: [P1, P5]
- **severity**: warning
- **context**: Sequence documentation, API flow descriptions

### AP-012

- **id**: AP-012
- **type**: anti-pattern
- **pattern**: Avoided synonym "commence" for "start"
- **non_ste**: Commence the build pipeline after the tests pass in the staging environment.
- **ste**: Start the build pipeline after the tests pass in the staging environment.
- **violates**: [P1]
- **severity**: error
- **context**: CI/CD pipeline documentation

### AP-013

- **id**: AP-013
- **type**: anti-pattern
- **pattern**: Avoided synonym "terminate" for "stop"
- **non_ste**: Terminate the background worker before you release the database connection to prevent locks.
- **ste**: Stop the background worker before you release the database connection to prevent locks.
- **violates**: [P1]
- **severity**: error
- **context**: Operations runbooks, shutdown procedures

### AP-014

- **id**: AP-014
- **type**: anti-pattern
- **pattern**: Contradictory instructions in the same section
- **non_ste**: Always enable caching for the reports endpoint. Never enable caching for the reports endpoint because it returns user-specific data.
- **ste**: Enable caching for the reports endpoint only when the response is identical for all users. Do not enable caching when the response contains user-specific data.
- **violates**: [P1, P8]
- **severity**: blocking
- **context**: Configuration reference, caching documentation

### AP-015

- **id**: AP-015
- **type**: anti-pattern
- **pattern**: Regional spelling inconsistency
- **non_ste**: Customise the serialise function to normalise the colour values before you initialise the widget.
- **ste**: Customize the serialize function to normalize the color values before you initialize the widget.
- **violates**: [P1]
- **severity**: error
- **context**: Library documentation, SDK reference

### AP-016

- **id**: AP-016
- **type**: anti-pattern
- **pattern**: Slang and informal phrasing
- **non_ste**: Just spin up a quick instance and hack the config until the thing stops crashing.
- **ste**: Start an instance and edit the configuration until the application stops crashing.
- **violates**: [P1, P4]
- **severity**: error
- **context**: Internal troubleshooting docs, incident notes

### AP-017

- **id**: AP-017
- **type**: anti-pattern
- **pattern**: Undefined technical term in README
- **non_ste**: The handler emits a webhook to the broker on each mutation event.
- **ste**: The handler sends an HTTP request to the message broker on each data change event. The broker distributes the request to subscribers.
- **violates**: [P1, P8]
- **severity**: error
- **context**: Project README files, quick-start guides

### AP-018

- **id**: AP-018
- **type**: anti-pattern
- **pattern**: Weak style — verbose phrasing
- **non_ste**: In order to be able to make use of the new logging feature it is necessary to carry out an update of the agent to the most recent version.
- **ste**: To use the new logging feature, update the agent to the latest version.
- **violates**: [P4]
- **severity**: info
- **context**: Release notes, upgrade documentation

### AP-019

- **id**: AP-019
- **type**: anti-pattern
- **pattern**: Synonym for an approved term
- **non_ste**: The module obtains the credentials and subsequently dispatches the request to the upstream service.
- **ste**: The module gets the credentials and then sends the request to the upstream service.
- **violates**: [P1]
- **severity**: info
- **context**: Integration documentation, module reference

### AP-020

- **id**: AP-020
- **type**: anti-pattern
- **pattern**: Avoided synonym "employ" with nominalization
- **non_ste**: Employ the prepared statement to effect the retrieval of rows from the table in a safe manner.
- **ste**: Use the prepared statement to get rows from the table safely.
- **violates**: [P1, P4]
- **severity**: error
- **context**: Database access documentation, query guides
