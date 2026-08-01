# Level 4 — Reference Dictionary (A–Z)

> **Source:** `ste-code/final/rules/a-dictionary.md` — the complete STE-Code adapted dictionary (A–Z).
> **Adapted from:** ASD-STE100 Issue 9, Part 2 — Dictionary (pages 149–434), with aerospace examples replaced by code-domain examples.
> **Tier:** Level 4 — full reference catalogue. This is the LLM-optimized distillation: the Original / Code-domain / Ref boilerplate is dropped; each entry keeps its approval status and its STE / Non-STE code-example pair(s).

## How to read this dictionary

- **`✓`** after a word = approved in STE-Code. **`✗`** = not approved; the STE / Non-STE pair shows the approved alternative to use.
- **(v)** verb · **(n)** noun · **(adj)** adjective · **(adv)** adverb · **(prep)** preposition · **(conj)** conjunction · **(pron)** pronoun · **(art)** article · **(TN)** code-domain Technical Noun · **(TV)** code-domain Technical Verb.
- Each entry lists the approval status, then `STE:` (approved form) and `Non-STE:` (the form to avoid) example pairs.
- `For other meanings, use: X, Y` points to approved words for distinct senses of the same spelling.
- `(retained)` marks a word kept from the source standard with no direct code-domain equivalent.

Use this list to choose approved words when an LLM generates code documentation (API docs, commit messages, README sections, code comments). Prefer approved words; when a word is marked `✗`, rewrite with the STE form shown.

---

## How  ✓


# A

## A (art)  ✓

- STE: A config file is included in the root directory.  |  Non-STE: Config files included in root directory.

## ABANDON (v)  ✗

Not approved. Use the STE form below.
- STE: If the build fails, stop the deployment pipeline.  |  Non-STE: If the build fails, abandon the deployment pipeline.
- STE: If the values are incorrect, terminate the test run.  |  Non-STE: If the values are incorrect, abandon the test procedure.

## ABILITY (n)  ✗

Not approved. Use the STE form below.
- STE: One configuration can handle requests for all the endpoints.  |  Non-STE: One configuration has the ability to handle requests for all the endpoints.

## ABLE (adj)  ✗

Not approved. Use the STE form below.
- STE: If you can run the script, do the applicable checks.  |  Non-STE: If you are able to run the script, do the applicable checks.

## ABNORMAL (adj)  ✗

Not approved. Use the STE form below.
- STE: Watch for unusual log entries.  |  Non-STE: Watch for abnormal log entries.
- STE: If you find an incorrect value in the output, do a debug run.  |  Non-STE: If you find an abnormal value in the output, do a debug run.

## ABNORMALITY (n)  ✗

Not approved. Use the STE form below.
- STE: Examine the reported stack trace for bugs.  |  Non-STE: Examine the reported stack trace for abnormalities.

## ABOUT (prep)  ✓

- STE: For data about the configuration of the module, refer to the README.  |  Non-STE: For data regarding the configuration of the module, refer to the README.
- STE: The build takes approximately 5 minutes.  |  Non-STE: The build takes about 5 minutes.
- STE: This document covers topics around testing and deployment.  |  Non-STE: This document covers topics about testing and deployment.
- For other meanings, use: APPROXIMATELY (adv), AROUND (prep)

## ABOVE (prep)  ✓

- STE: Move the cursor above the target line.  |  Non-STE: Move the cursor to a position above the target line.
- STE: The response time must be more than 200 ms.  |  Non-STE: The response time must be above 200 ms.
- For other meanings, use: MORE THAN

## ABRASIVE (adj)  (retained)

Retained from the source standard (no direct code-domain equivalent).

## ABRUPT (adj)  ✗

Not approved. Use the STE form below.
- STE: The watchdog prevents sudden shutdown of the service.  |  Non-STE: The watchdog prevents abrupt shutdown of the service.
- STE: If the process stops suddenly, examine the logs.  |  Non-STE: If the process comes to an abrupt stop, examine the logs.

## ABSENCE (n)  ✗

Not approved. Use the STE form below.
- STE: If none of the tests fail, continue the deployment.  |  Non-STE: In the absence of test failures, continue the deployment.
- STE: If the tests are not failing, continue the deployment.  |  Non-STE: In the absence of test failures, continue the deployment.
- STE: If there is no error in the output, continue the procedure.  |  Non-STE: In the absence of errors in the output, continue the procedure.

## ABSENT (adj)  ✗

Not approved. Use the STE form below.
- STE: If one or more files are missing, add an entry in the changelog.  |  Non-STE: If one or more files are absent, add an entry in the changelog.

## ABSOLUTELY (adv)  ✗

Not approved. Use the STE form below.
- STE: Make sure that the connection is fully established.  |  Non-STE: Make sure that the connection is absolutely established.

## ABSORB (v)  ✓

- STE: The buffer absorbs the input data.  |  Non-STE: The buffer takes up the input data.
- STE: The cache layer absorbs the load from repeated queries.  |  Non-STE: The cache layer mitigates the load from repeated queries.

## ABSORPTION (n)  ✗

Not approved. Use the STE form below.
- STE: Measure the time that is necessary for the log system to absorb the incoming events.  |  Non-STE: Measure the rate of absorption of incoming events by the log system.

## ABUNDANT (adj)  ✗

Not approved. Use the STE form below.
- STE: Log the errors with a large quantity of context data.  |  Non-STE: Log the errors with abundant context data.

## ABUT (v)  ✗

Not approved. Use the STE form below.
- STE: The widget touches the boundary of the container.  |  Non-STE: The widget abuts the boundary of the container.

## ACCELERATE (v)  ✗

Not approved. Use the STE form below.
- STE: A larger buffer size increases the speed of data transfer.  |  Non-STE: A larger buffer size accelerates data transfer.
- STE: To make the build process faster, use parallel compilation.  |  Non-STE: To accelerate the build process, use parallel compilation.

## ACCEPT (v)  ✓

- STE: Accept the pull request if it passes all checks.  |  Non-STE: Merge the pull request if it passes all checks.

## ACCEPTABLE (adj)  ✗

Not approved. Use the STE form below.
- STE: A response time of 200 ms is permitted.  |  Non-STE: A response time of 200 ms is acceptable.
- STE: If the condition of the build is not satisfactory, run it again.  |  Non-STE: If the condition of the build is not acceptable, run it again.
- STE: Before you deploy the update, make sure that it is ready.  |  Non-STE: Before you deploy the update, make sure that it is acceptable.

## ACCEPTANCE (n)  ✗

Not approved. Use the STE form below.
- STE: Before you accept the merge request, do the specified review checklist.  |  Non-STE: Before acceptance of the merge request, do the specified review checklist.

## ACCESS (n)  ✓

- STE: Get access to the repository for the authentication module.  |  Non-STE: Access the repository for the authentication module.

## ACCESSIBLE (adj)  ✗

Not approved. Use the STE form below.
- STE: Scroll the view until you can get access to the functions that have public annotations.  |  Non-STE: Scroll the view until the functions with public annotations are accessible.

## ACCIDENT (n)  ✓

- STE: To prevent accidents, make sure that the backups are configured.  |  Non-STE: To prevent accidents, ensure that backups are in place.

## ACCIDENTAL (adj)  ✓

- STE: To prevent accidental deletion of the files, confirm the operation.  |  Non-STE: To prevent inadvertent deletion of the files, confirm the operation.

## ACCIDENTALLY (adv)  ✓

- STE: If you accidentally press the delete key, restore the file from the recycle bin.  |  Non-STE: If you inadvertently press the delete key, restore the file from the recycle bin.

## ACCOMMODATE (v)  ✗

Not approved. Use the STE form below.
- STE: Different configurations let you handle different types of input.  |  Non-STE: Different configurations accommodate different types of input.

## ACCOMPLISH (v)  ✗

Not approved. Use the STE form below.
- STE: Do this build step first.  |  Non-STE: Accomplish this build step first.
- STE: The pipeline must complete this stage in 5 minutes.  |  Non-STE: The pipeline must accomplish this stage in 5 minutes.

## ACCORDING  ✗

Not approved. Use the STE form below.
- STE: To configure the module, refer to the developer's guide.  |  Non-STE: Configure the module according to the developer's guide.

## ACCOUNT  ✗

Not approved. Use the STE form below.
- STE: Make sure that you track all dependencies and packages.  |  Non-STE: All dependencies and packages must be accounted for.

## ACCUMULATE (v)  ✗

Not approved. Use the STE form below.
- STE: If logs collect in the buffer, flush them.  |  Non-STE: If logs accumulate in the buffer, flush them.

## ACCUMULATION (n)  ✗

Not approved. Use the STE form below.
- STE: Remove large quantities of obsolete logs.  |  Non-STE: Remove large accumulations of obsolete logs.
- STE: If errors collect frequently, examine the connection for issues.  |  Non-STE: If accumulation of errors is frequent, examine the connection for issues.

## ACCURACY (n)  ✗

Not approved. Use the STE form below.
- STE: The precision of the calculation can change.  |  Non-STE: The accuracy of the calculation can change.

## ACCURATE (adj)  ✓

- STE: The measurement must be accurate.  |  Non-STE: The measurement must be precise.
- STE: Apply the patch accurately on the target branch.  |  Non-STE: Put the patch accurately on the target branch.

## ACHIEVE (v)  ✗

Not approved. Use the STE form below.
- STE: Set the flag to get maximum performance.  |  Non-STE: Set the flag to achieve maximum performance.

## ACQUIRE (v)  ✗

Not approved. Use the STE form below.
- STE: The module gets this data from three endpoints.  |  Non-STE: The module acquires this data from three endpoints.

## ACRID (adj)  ✗

Not approved. Use the STE form below.

## ACROSS (prep)  ✓

- STE: Search across all modules for the deprecated function.  |  Non-STE: Search all modules for the deprecated function.

## ACT (v)  ✗

Not approved. Use the STE form below.
- STE: The event trigger invokes the handler.  |  Non-STE: The event trigger acts on the handler.

## ACTION (n)  ✗

Not approved. Use the STE form below.
- STE: Do the steps that follow.  |  Non-STE: Do the following actions.
- STE: Do not do this procedure in the production environment.  |  Non-STE: This action must not be done in the production environment.
- STE: Do this task in the staging environment.  |  Non-STE: Do this action in the staging environment.

## ACTIVATE (v)  ✓

- STE: The build pipeline activates the deployment mode.  |  Non-STE: The build pipeline triggers the deployment mode.
- STE: Start the container.  |  Non-STE: Activate the container.
- For other meanings, use: START (v)

## ACTIVE (adj)  ✓

- STE: Read the config from the active branch.  |  Non-STE: Read the config from the current branch.

## ACTIVITY (n)  ✗

Not approved. Use the STE form below.
- STE: A contributor can do these review tasks.  |  Non-STE: A contributor can do these review activities.
- STE: Do this procedure in the development branch.  |  Non-STE: Do this activity in the development branch.
- STE: Do this work in a clean workspace.  |  Non-STE: Do this activity in a clean workspace.

## ACTUATE (v)  ✗

Not approved. Use the STE form below.
- STE: Start the server.  |  Non-STE: Actuate the server.
- STE: Run the script.  |  Non-STE: Actuate the script.

## ACTUATION (n)  ✗

Not approved. Use the STE form below.
- STE: Monitor the operation of the background worker.  |  Non-STE: Monitor the actuation of the background worker.

## ADAPT (v)  ✓

- STE: Adapt the connector to the database schema.  |  Non-STE: Adjust the connector to fit the database schema.
- STE: The middleware layer adapts to the protocol of the connected services.  |  Non-STE: The middleware layer conforms to the protocol of the connected services.

## ADD (v)  ✓

- STE: Add 5 lines of configuration to the file.  |  Non-STE: Append 5 lines of configuration to the file.

## ADDITION (n)  ✗

Not approved. Use the STE form below.
- STE: To get the correct behavior, add special flags, as necessary.  |  Non-STE: To get the correct behavior through the addition of special flags, as necessary.

## ADDITIONAL (adj)  ✗

Not approved. Use the STE form below.
- STE: This section gives more information about deployment.  |  Non-STE: This section gives additional information about deployment.

## ADEQUATE (adj)  ✗

Not approved. Use the STE form below.
- STE: Make sure that buffers have sufficient capacity and throughput.  |  Non-STE: Make sure that buffers have adequate capacity and throughput.

## ADHERE (v)  ✗

Not approved. Use the STE form below.
- STE: The patch must attach correctly.  |  Non-STE: The patch must adhere correctly.
- STE: Obey the coding standards.  |  Non-STE: Adhere to the coding standards.

## ADHESION (n)  ✗

Not approved. Use the STE form below.

## ADJACENT (adj)  ✓

- STE: Do not modify the adjacent function.  |  Non-STE: Do not modify the function that is next to it.
- STE: The config file is located adjacent to the main module.  |  Non-STE: The config file is located next to the main module.

## ADJOINING (adj)  ✗

Not approved. Use the STE form below.
- STE: Align the imports with the adjacent modules.  |  Non-STE: Align the imports with the adjoining modules.

## ADJUST (v)  ✓

- STE: Adjust the timeout to the value given in Table 1.  |  Non-STE: Tune the timeout to the value given in Table 1.
- STE: The auto-scaler adjusts to sudden changes in load.  |  Non-STE: The auto-scaler adapts to sudden changes in load.

## ADJUSTABLE (adj)  ✓

- STE: The two parameters are adjustable.  |  Non-STE: The two parameters can be tuned.
- STE: Make sure that the adjustment is in the limits given in Table 1.  |  Non-STE: Make sure that the tuning is in the limits given in Table 1.

## ADMIT (v)  ✗

Not approved. Use the STE form below.
- STE: Open the port to let traffic go into the container.  |  Non-STE: Open the port to admit traffic into the container.

## ADOPT (v)  ✗

Not approved. Use the STE form below.
- STE: If the build fails, use this fallback script.  |  Non-STE: Adopt this fallback script if the build fails.

## ADVANCE (n)  ✗

Not approved. Use the STE form below.
- STE: The forward movement of the iterator must be sequential.  |  Non-STE: The advance of the iterator must be sequential.

## ADVANCE (v)  ✗

Not approved. Use the STE form below.
- STE: Set the pointer to the next node.  |  Non-STE: Advance the pointer to the next node.
- STE: Move the cursor forward.  |  Non-STE: Advance the cursor.

## ADVERSE (adj)  ✗

Not approved. Use the STE form below.
- STE: Refer to Section 6 for instructions about how to handle bad network conditions.  |  Non-STE: Refer to Section 6 for instructions about how to handle adverse network conditions.

## ADVISABLE (adj)  ✗

Not approved. Use the STE form below.
- STE: The technical lead recommends that you rebuild the containers at intervals of two weeks.  |  Non-STE: It is advisable to rebuild the containers at intervals of two weeks.

## ADVISE (v)  ✗

Not approved. Use the STE form below.
- STE: Tell the reviewer that the changes are ready.  |  Non-STE: Advise the reviewer that the changes are ready.
- STE: The security officer recommends the applicable authentication protocol.  |  Non-STE: The security officer advises on the applicable authentication protocol.

## AFFECT (v)  ✗

Not approved. Use the STE form below.
- STE: Thread locks have an unwanted effect on the scheduler.  |  Non-STE: Thread locks affect the scheduler.

## AFT (adj)  ✓


## AFTER (conj)  ✓

- STE: After you deploy the update, do a smoke test.  |  Non-STE: Following deployment of the update, do a smoke test.

## AGAIN (adv)  ✓

- STE: Run the test again.  |  Non-STE: Rerun the test.

# B

## BACK (adj)  ✓

- STE: Revert to the back version.  |  Non-STE: Revert to the previous version.
- STE: Navigate back to the previous page.  |  Non-STE: Go backwards to the previous page.

## BACK  ✗

Not approved. Use the STE form below.
- STE: Save the database before the migration.  |  Non-STE: Back up the database before the migration.
- STE: Copy the configuration files.  |  Non-STE: Back up the configuration files.

## BAD (adj)  ✓

- STE: Refer to Section 6 for instructions about how to handle bad build states.  |  Non-STE: Refer to Section 6 for instructions about how to handle unsatisfactory build states.

## BALANCE (n)  ✓

- STE: Make sure that the load is in balance across all nodes.  |  Non-STE: Make sure that the load is balanced across all nodes.
- STE: Balance the workload across all workers.  |  Non-STE: Distribute the workload across all workers.

## BASE (n)  ✗

Not approved. Use the STE form below.
- STE: The foundation of the architecture is the data layer.  |  Non-STE: The base of the architecture is the data layer.
- STE: Start from the root of the project.  |  Non-STE: Start from the base of the project.

## BE (v)  ✓

- STE: If there is an error in the log, restart the service.  |  Non-STE: If an error exists in the log, restart the service.
- STE: Unhandled exceptions are dangerous.  |  Non-STE: Unhandled exceptions constitute a danger.

## BECAUSE (conj)  ✓

- STE: Do not use raw input, because it is a security risk.  |  Non-STE: Do not use raw input, since it is a security risk.

## BECOME (v)  ✓

- STE: The connection becomes unstable.  |  Non-STE: The connection turns unstable.

## BEFORE (conj)  ✓

- STE: Before you run the migration, read the release notes.  |  Non-STE: Prior to running the migration, read the release notes.

## BEGIN (v)  ✓

- STE: Begin the build process.  |  Non-STE: Initiate the build process.

## BELOW (prep)  ✓

- STE: See the example below the code block.  |  Non-STE: See the example beneath the code block.

## BEND (v)  ✓


## BETWEEN (prep)  ✓

- STE: Put the middleware between the client and the server.  |  Non-STE: Insert the middleware between the client and the server.

## BLOCK (n)  ✓

- STE: Put a comment block above the function.  |  Non-STE: Add documentation above the function.

## BOND (v)  ✓


## BOTTOM (n)  ✓

- STE: Scroll to the bottom of the file.  |  Non-STE: Scroll to the end of the file.
- STE: The bottom layer of the stack is the database.  |  Non-STE: The lowest layer of the stack is the database.

## BRACKET (n)  ✓

- STE: Use square brackets for array access.  |  Non-STE: Use the bracket notation for array access.

## BREAK (v)  ✓

- STE: Do not break the public API.  |  Non-STE: Do not cause breaking changes to the public API.
- STE: Break out of the loop when the flag is set.  |  Non-STE: Exit the loop when the flag is set.

## BRING (v)  ✗

Not approved. Use the STE form below.
- STE: Get the dependencies into the container.  |  Non-STE: Bring the dependencies into the container.

## BROAD (adj)  ✗

Not approved. Use the STE form below.
- STE: Wide test coverage.  |  Non-STE: Broad test coverage.

## BUG (n)  ✓

- STE: Use the bug tracker to log defects.  |  Non-STE: Use the issue tracker to log defects.

## BUILD (v)  ✗

Not approved. Use the STE form below.
- STE: Compile the project.  |  Non-STE: Build the project.

## BURN (v)  ✓

- STE: Burn the ISO image to the USB drive.  |  Non-STE: Write the ISO image to the USB drive.

## BUT (conj)  ✓

- STE: The build passes, but the tests fail.  |  Non-STE: The build passes, however the tests fail.

## BY (prep)  ✓

- STE: Build the project by the CMake tool.  |  Non-STE: Build the project using CMake.
- STE: Authenticate by OAuth.  |  Non-STE: Authenticate via OAuth.

## BYTE (n)  ✓

- STE: The buffer holds 1024 bytes.  |  Non-STE: The buffer has a size of 1024 bytes.

# C

## CALCULATE (v)  ✓

- STE: Calculate the checksum of the file.  |  Non-STE: Compute the checksum of the file.

## CALL (v)  ✗

Not approved. Use the STE form below.
- STE: Name the function "init."  |  Non-STE: Call the function "init."
- STE: Contact the administrator.  |  Non-STE: Call the administrator.

## CAN (v)  ✓

- STE: A misconfiguration can cause a crash.  |  Non-STE: A misconfiguration could cause a crash.
- STE: You can run the script after the build is completed.  |  Non-STE: You are able to run the script after the build is completed.

## CANCEL (v)  ✓

- STE: Cancel the deployment pipeline.  |  Non-STE: Abort the deployment pipeline.

## CANNOT (v)  ✓

- STE: You cannot access this endpoint without authentication.  |  Non-STE: You are unable to access this endpoint without authentication.

## CAPABLE (adj)  ✗

Not approved. Use the STE form below.
- STE: The service can recover from failures automatically.  |  Non-STE: The service is capable of recovering from failures automatically.

## CARE (n)  ✗

Not approved. Use the STE form below.
- STE: Be careful when you change the configuration.  |  Non-STE: Take care when changing the configuration.

## CARRY (v)  ✗

Not approved. Use the STE form below.
- STE: Move the data to the cache.  |  Non-STE: Carry the data to the cache.

## CARRY  ✗

Not approved. Use the STE form below.
- STE: Do the review.  |  Non-STE: Carry out the review.

## CASE (n)  ✗

Not approved. Use the STE form below.
- STE: If the flag is true, log the event.  |  Non-STE: In case the flag is true, log the event.
- STE: Add a switch case for the error state.  |  Non-STE: Handle the error case.

## CATCH (v)  ✓

- STE: Catch the exception and log it.  |  Non-STE: Trap the exception and log it.

## CAUSE (v)  ✓

- STE: The null pointer caused the crash.  |  Non-STE: The null pointer resulted in the crash.

## CAUTION (n)  ✓

- STE: Obey the cautions in this README.  |  Non-STE: Follow the cautions in this README.

## CENTER (n)  ✓

- STE: Align the text to the center.  |  Non-STE: Center the text.

## CHANGE (v)  ✓

- STE: Change the function signature.  |  Non-STE: Modify the function signature.
- STE: Record the changes in the changelog.  |  Non-STE: Log the changes in the changelog.

## CHECK (n)  ✓

- STE: Do a check of the input values.  |  Non-STE: Validate the input values.

## CHECK (v)  ✗

Not approved. Use the STE form below.
- STE: Do a check of the values.  |  Non-STE: Check the values.
- STE: Verify the data integrity.  |  Non-STE: Check the data integrity.

## CHOOSE (v)  ✗

Not approved. Use the STE form below.
- STE: Select the correct configuration.  |  Non-STE: Choose the correct configuration.

## CLEAN (v)  ✓

- STE: Clean the temporary files.  |  Non-STE: Delete the temporary files.

## CLEAR (adj)  ✓

- STE: A clear code path for the request.  |  Non-STE: An unobstructed code path for the request.
- STE: Clear documentation for the API.  |  Non-STE: Understandable documentation for the API.

## CLICK (n)  ✓

- STE: Click the "Submit" button.  |  Non-STE: Press the "Submit" button.

## CLOSE (v)  ✓

- STE: Close the file handle.  |  Non-STE: Release the file handle.

## CODE (n)  ✓

- STE: The code is in the `src/` directory.  |  Non-STE: The source is in the `src/` directory.

## COLLECT (v)  ✓

- STE: Collect the metrics from all nodes.  |  Non-STE: Gather the metrics from all nodes.

## COME (v)  ✓

- STE: When the service comes online, start the tests.  |  Non-STE: When the service starts, start the tests.

## COMMENT (n)  ✓

- STE: Add a comment to explain the algorithm.  |  Non-STE: Document the algorithm in the code.

## COMMIT (v)  ✓

- STE: Commit the changes to the repository.  |  Non-STE: Save the changes to the repository.

## COMPARE (v)  ✓

- STE: Compare the hash value with the expected hash.  |  Non-STE: Check the hash value against the expected hash.

## COMPATIBLE (adj)  ✓

- STE: The library is compatible with version 3.0.  |  Non-STE: The library works with version 3.0.

## COMPILE (v)  ✗

Not approved. Use the STE form below.
- STE: Compile the source files.  |  Non-STE: Build the source files.

## COMPLETE (v)  ✓

- STE: Complete the setup wizard.  |  Non-STE: Finish the setup wizard.

## COMPONENT (n)  ✓

- STE: The component is imported in the module.  |  Non-STE: The component is used in the module.

## COMPRESS (v)  ✓

- STE: Compress the log files before archiving.  |  Non-STE: Zip the log files before archiving.

## CONDITION (n)  ✓

- STE: The condition of the build is satisfactory.  |  Non-STE: The build state is good.
- STE: If the condition is true, continue.  |  Non-STE: If the conditional evaluates to true, continue.

## CONFIGURATION (n)  ✓

- STE: The configuration file is in YAML format.  |  Non-STE: The config file is in YAML format.

## CONFIRM (v)  ✗

Not approved. Use the STE form below.
- STE: Make sure that the build is successful.  |  Non-STE: Confirm that the build is successful.

## CONNECT (v)  ✓

- STE: Connect the client to the server.  |  Non-STE: Establish a connection between the client and the server.

## CONTAIN (v)  ✓

- STE: The module contains the helper functions.  |  Non-STE: The module includes the helper functions.

## CONTACT (v)  ✓

- STE: Contact the system administrator.  |  Non-STE: Get in touch with the system administrator.

## CONTINUE (v)  ✓

- STE: If the build passes, continue the deployment.  |  Non-STE: If the build passes, proceed with the deployment.

## CONTROL (n)  ✓

- STE: The control of the access is role-based.  |  Non-STE: Access is role-based.
- STE: Control the workflow with the dashboard.  |  Non-STE: Manage the workflow with the dashboard.

## COPY (v)  ✓

- STE: Copy the config to the staging environment.  |  Non-STE: Duplicate the config to the staging environment.

## CORRECT (adj)  ✓

- STE: Make sure that the test results are correct.  |  Non-STE: Verify that the test results are correct.

## CORRECTLY (adv)  ✓

- STE: Make sure that the package is correctly installed.  |  Non-STE: Ensure the package is correctly installed.

## COUNT (v)  ✓

- STE: Count the records in the database.  |  Non-STE: Get the count of records in the database.

## COVER (n)  ✓


## CRASH (v)  ✓

- STE: If the application crashes, read the logs.  |  Non-STE: If the application fails, read the logs.

## CREATE (v)  ✓

- STE: Create a new instance of the class.  |  Non-STE: Instantiate a new object of the class.

## CUT (v)  ✓

- STE: Cut the text and paste it in the new location.  |  Non-STE: Move the text to the new location.

# D

## DAMAGE (n)  ✓

- STE: The damage to the data is irreversible.  |  Non-STE: The data corruption is irreversible.

## DANGER (n)  ✗

Not approved. Use the STE form below.
- STE: This operation has a risk of data loss.  |  Non-STE: There is a danger of data loss with this operation.

## DANGEROUS (adj)  ✓

- STE: This command is dangerous.  |  Non-STE: This command poses a danger.

## DATA (n)  ✓

- STE: The data is stored in the cache.  |  Non-STE: The information is stored in the cache.

## DEACTIVATE (v)  ✓

- STE: Deactivate the background worker.  |  Non-STE: Disable the background worker.

## DEBUG (v)  ✓

- STE: Debug the application with the attached profiler.  |  Non-STE: Troubleshoot the application with the attached profiler.

## DECREASE (v)  ✓

- STE: Decrease the timeout value.  |  Non-STE: Lower the timeout value.

## DEEP (adj)  ✓

- STE: Deep directory structure.  |  Non-STE: Nested directory structure.

## DEFAULT (n)  ✓

- STE: The default value is 8080.  |  Non-STE: The initial value is 8080.

## DEFECT (n)  ✓

- STE: Log the defect in the tracking system.  |  Non-STE: Log the bug in the tracking system.

## DEFINE (v)  ✓

- STE: The header file defines the interface.  |  Non-STE: The header file declares the interface.

## DELETE (v)  ✗

Not approved. Use the STE form below.
- STE: Remove the file from the directory.  |  Non-STE: Delete the file from the directory.

## DEPLOY (v)  ✓

- STE: Deploy the application to production.  |  Non-STE: Release the application to production.

## DEPRECATED (adj)  ✓

- STE: The deprecated function will be removed in version 4.0.  |  Non-STE: The outdated function will be removed in version 4.0.

## DESIGN (n)  ✓

- STE: The design of the API follows REST principles.  |  Non-STE: The architecture of the API follows REST principles.

## DESTROY (v)  ✗

Not approved. Use the STE form below.
- STE: Break the old session.  |  Non-STE: Destroy the old session.

## DEVELOP (v)  ✓

- STE: Develop the feature in a separate branch.  |  Non-STE: Build the feature in a separate branch.

## DIFFERENT (adj)  ✓

- STE: The two implementations have different performance.  |  Non-STE: The two implementations differ in performance.

## DIMENSION (n)  ✓

- STE: The array has three dimensions.  |  Non-STE: The array is three-dimensional.

## DIRECTORY (n)  ✓

- STE: The source files are in the `src/` directory.  |  Non-STE: The source files are in the `src/` folder.

## DISABLE (v)  ✓

- STE: Disable the feature flag.  |  Non-STE: Turn off the feature flag.

## DISCARD (v)  ✓

- STE: Discard the deprecated code.  |  Non-STE: Remove the deprecated code.

## DISCONNECT (v)  ✓

- STE: Disconnect the socket.  |  Non-STE: Close the socket.

## DISPLAY (v)  ✓

- STE: The terminal displays the log output.  |  Non-STE: The terminal shows the log output.

## DIVIDE (v)  ✓

- STE: Divide the tasks among the workers.  |  Non-STE: Distribute the tasks among the workers.

## DO (v)  ✓

- STE: Do the build step.  |  Non-STE: Execute the build step.

## DOCUMENT (v)  ✓

- STE: Document the public API.  |  Non-STE: Write docs for the public API.

## DOWN (adv)  ✓

- STE: Scroll down the page.  |  Non-STE: Scroll to the lower part of the page.
- STE: The server is down.  |  Non-STE: The server is not operational.

## DOWNLOAD (v)  ✓

- STE: Download the package from the registry.  |  Non-STE: Get the package from the registry.

## DRAIN (v)  ✓

- STE: Drain the connection pool.  |  Non-STE: Empty the connection pool.

## DRAW (v)  ✓

- STE: Draw the architecture diagram.  |  Non-STE: Create the architecture diagram.

## DROP (v)  ✓

- STE: Drop the table from the database.  |  Non-STE: Delete the table from the database.

## DRY (adj)  ✓


# E

## EACH (adj)  ✓

- STE: Each module has a README file.  |  Non-STE: Every module has a README file.

## EASY (adj)  ✓

- STE: The setup is easy.  |  Non-STE: The setup is straightforward.

## EDIT (v)  ✓

- STE: Edit the configuration file with a text editor.  |  Non-STE: Modify the configuration file with a text editor.

## EFFECT (n)  ✓

- STE: The effect of the change is small.  |  Non-STE: The impact of the change is small.

## EJECT (v)  ✓

- STE: Eject the volume.  |  Non-STE: Unmount the volume.

## ELEMENT (n)  ✓

- STE: Each element of the list has an index.  |  Non-STE: Each item of the list has an index.

## ELSE (adv)  ✓

- STE: If the value is null, return 0; else return the value.  |  Non-STE: If the value is null, return 0; otherwise return the value.

## EMPTY (adj)  ✓

- STE: An empty string.  |  Non-STE: A zero-length string.

## ENABLE (v)  ✓

- STE: Enable the debug mode.  |  Non-STE: Turn on the debug mode.

## END (n)  ✓

- STE: The end of the file.  |  Non-STE: The final byte of the file.
- STE: End the session.  |  Non-STE: Terminate the session.

## ENSURE (v)  ✗

Not approved. Use the STE form below.
- STE: Make sure that the database is connected.  |  Non-STE: Ensure that the database is connected.

## ENTER (v)  ✗

Not approved. Use the STE form below.
- STE: Type your password.  |  Non-STE: Enter your password.

## ENVIRONMENT (n)  ✓

- STE: The staging environment is a copy of production.  |  Non-STE: The staging setup is a copy of production.

## EQUAL (adj)  ✓

- STE: The two hashes are equal.  |  Non-STE: The two hashes are the same.
- STE: The result equals zero.  |  Non-STE: The result is zero.

## ERASE (v)  ✓

- STE: Erase the sensitive data from memory.  |  Non-STE: Wipe the sensitive data from memory.

## ERROR (n)  ✓

- STE: The error occurred at line 42.  |  Non-STE: The issue occurred at line 42.

## ESTABLISH (v)  ✗

Not approved. Use the STE form below.
- STE: Make a connection.  |  Non-STE: Establish a connection.

## EVALUATE (v)  ✓

- STE: Evaluate the expression at runtime.  |  Non-STE: Compute the expression at runtime.

## EVENT (n)  ✓

- STE: The event triggers the callback.  |  Non-STE: The event fires the callback.

## EXAMINE (v)  ✓

- STE: Examine the code for security issues.  |  Non-STE: Review the code for security issues.

## EXAMPLE (n)  ✓

- STE: This is an example of a correct API call.  |  Non-STE: This demonstrates a correct API call.

## EXCEPT (prep)  ✗

Not approved. Use the STE form below.
- STE: All modules except the database module are available.  |  Non-STE: All modules other than the database module are available.

## EXECUTE (v)  ✓

- STE: Execute the script from the terminal.  |  Non-STE: Run the script from the terminal.

## EXPAND (v)  ✓

- STE: Expand the macro at compile time.  |  Non-STE: The macro is substituted at compile time.

## EXPLAIN (v)  ✗

Not approved. Use the STE form below.
- STE: Describe the error condition.  |  Non-STE: Explain the error condition.

## EXPORT (v)  ✓

- STE: Export the function from the library.  |  Non-STE: Make the function available from the library.

## EXTEND (v)  ✓

- STE: Extend the base class to add new methods.  |  Non-STE: Subclass the base class to add new methods.

# F

## FAIL (v)  ✓

- STE: If the test fails, examine the logs.  |  Non-STE: If the test does not pass, examine the logs.

## FAILURE (n)  ✗

Not approved. Use the STE form below.
- STE: If the service stops, restart it.  |  Non-STE: In case of service failure, restart it.

## FALL (v)  ✓


## FALSE (adj)  ✓

- STE: If the condition is false, skip the block.  |  Non-STE: If the condition does not hold, skip the block.

## FAST (adj)  ✓

- STE: Fast response time.  |  Non-STE: Low latency.

## FATAL (adj)  ✓

- STE: A fatal error occurred.  |  Non-STE: A critical error occurred.

## FETCH (v)  ✓

- STE: Fetch the records from the database.  |  Non-STE: Retrieve the records from the database.

## FIELD (n)  ✓

- STE: The `email` field of the form must be validated.  |  Non-STE: The `email` input of the form must be validated.

## FILE (n)  ✓

- STE: The configuration file is in TOML format.  |  Non-STE: The config is in TOML format.

## FILL (v)  ✓

- STE: Fill the array with default values.  |  Non-STE: Initialize the array with default values.

## FILTER (n)  ✓

- STE: Filter the results by status.  |  Non-STE: Select only the results that match the status.

## FIND (v)  ✓

- STE: Find the root cause of the error.  |  Non-STE: Determine the root cause of the error.

## FINISH (v)  ✓

- STE: Finish the setup.  |  Non-STE: Complete the setup.

## FIRST (adj)  ✓

- STE: Define the variable first.  |  Non-STE: Initially define the variable.

## FIT (v)  ✗

Not approved. Use the STE form below.
- STE: Install the package.  |  Non-STE: Fit the package into the project.

## FIX (v)  ✓

- STE: Fix the memory leak.  |  Non-STE: Resolve the memory leak.

## FLAG (n)  ✓

- STE: Set the debug flag to true.  |  Non-STE: Enable the debug flag.

## FLOW (n)  ✓

- STE: The flow of data through the pipeline.  |  Non-STE: The data stream through the pipeline.
- STE: The data flows through the channel.  |  Non-STE: The data passes through the channel.

## FOLLOW (v)  ✗

Not approved. Use the STE form below.
- STE: Obey the coding guidelines.  |  Non-STE: Follow the coding guidelines.

## FOR (prep)  ✓

- STE: For examples, refer to the README.  |  Non-STE: To see examples, refer to the README.

## FORCE (n)  ✓

- STE: Force the application to restart.  |  Non-STE: Compel the application to restart.

## FORMAT (n)  ✓

- STE: The file format is JSON.  |  Non-STE: The file is in JSON.

## FORWARD (adv)  ✓

- STE: Move the pointer forward.  |  Non-STE: Advance the pointer.

## FREE (adj)  ✓

- STE: The code is free of errors.  |  Non-STE: The code has no errors.

## FROM (prep)  ✓

- STE: Import the module from the package.  |  Non-STE: Import the module out of the package.

## FULL (adj)  ✓

- STE: Full test suite.  |  Non-STE: Complete test suite.

## FUNCTION (n)  ✓

- STE: The function returns a string.  |  Non-STE: The method returns a string.
- STE: The function of the middleware is to authenticate requests.  |  Non-STE: The role of the middleware is to authenticate requests.

# G

## GET (v)  ✓

- STE: Get the data from the API.  |  Non-STE: Fetch the data from the API.
- STE: The service gets unstable under load.  |  Non-STE: The service becomes unstable under load.

## GIVE (v)  ✓

- STE: This section gives the build instructions for the module.  |  Non-STE: This section provides the build instructions for the module.

## GO (v)  ✓

- STE: Go to the next phase of the pipeline.  |  Non-STE: Proceed to the next phase of the pipeline.

## GOOD (adj)  ✓

- STE: Good test coverage.  |  Non-STE: Satisfactory test coverage.

## GROUP (n)  ✓

- STE: Group the tests by module.  |  Non-STE: Organize the tests by module.

# H

## HANDLE (v)  ✗

Not approved. Use the STE form below.
- STE: Process the exception.  |  Non-STE: Handle the exception.

## HAPPEN (v)  ✗

Not approved. Use the STE form below.
- STE: An exception occurred during initialization.  |  Non-STE: An exception happened during initialization.

## HARD (adj)  ✓

- STE: A hard limit on the number of connections.  |  Non-STE: A strict limit on the number of connections.

## HAVE (v)  ✓

- STE: The class has two methods.  |  Non-STE: The class contains two methods.

## HEAD (n)  ✓

- STE: The head of the queue.  |  Non-STE: The front of the queue.

## HELP (n)  ✓

- STE: This README helps you to set up the project.  |  Non-STE: This README assists you in setting up the project.

## HIGH (adj)  ✓

- STE: High load on the server.  |  Non-STE: Heavy load on the server.

## HIT (v)  ✓

- STE: Hit the endpoint with a GET request.  |  Non-STE: Send a GET request to the endpoint.

## HOLD (v)  ✓

- STE: Hold the lock until the operation completes.  |  Non-STE: Keep the lock until the operation completes.

## HOOK (n)  ✓

- STE: Use a pre-commit hook to validate the code.  |  Non-STE: Use a pre-commit script to validate the code.

## HOW (adv)  ✓

- STE: How to compile the project.  |  Non-STE: Instructions to compile the project.

# I

## IDENTIFY (v)  ✓

- STE: Identify the source of the memory leak.  |  Non-STE: Find the source of the memory leak.

## IF (conj)  ✓

- STE: If the status code is 500, retry the request.  |  Non-STE: In the event of a 500 status code, retry the request.

## IGNORE (v)  ✓

- STE: Ignore the case sensitivity.  |  Non-STE: Do not consider the case sensitivity.

## IMMEDIATELY (adv)  ✓

- STE: Restart the service immediately.  |  Non-STE: Restart the service right away.

## IMPLEMENT (v)  ✓

- STE: Implement the interface.  |  Non-STE: Code the interface.

## IMPORT (v)  ✓

- STE: Import the module at the top of the file.  |  Non-STE: Include the module at the top of the file.

## IMPORTANT (adj)  ✓

- STE: Important security note.  |  Non-STE: Critical security note.

## IN (prep)  ✓

- STE: In the directory `src/lib/`.  |  Non-STE: Within the directory `src/lib/`.

## INCLUDE (v)  ✓

- STE: The package includes the dependencies.  |  Non-STE: The package contains the dependencies.

## INCORRECT (adj)  ✓

- STE: Incorrect syntax.  |  Non-STE: Wrong syntax.

## INCREASE (v)  ✓

- STE: Increase the buffer size.  |  Non-STE: Make the buffer larger.

## INDEX (n)  ✓

- STE: The index of the element is 0.  |  Non-STE: The position of the element is 0.

## INDICATE (v)  ✗

Not approved. Use the STE form below.
- STE: The log shows the error type.  |  Non-STE: The log indicates the error type.

## INITIALIZE (v)  ✓

- STE: Initialize the variable to zero.  |  Non-STE: Set the variable to zero initially.

## INPUT (n)  ✓

- STE: Validate the user input.  |  Non-STE: Validate the data entered by the user.

## INSERT (v)  ✗

Not approved. Use the STE form below.
- STE: Put the record into the database.  |  Non-STE: Insert the record into the database.

## INSPECT (v)  ✗

Not approved. Use the STE form below.
- STE: Review the code for vulnerabilities.  |  Non-STE: Inspect the code for vulnerabilities.

## INSTALL (v)  ✓

- STE: Install the package with npm.  |  Non-STE: Set up the package with npm.

## INSTRUCTION (n)  ✓

- STE: Obey the instructions in the README.  |  Non-STE: Follow the instructions in the README.

## INTERFACE (n)  ✓

- STE: The interface defines three methods.  |  Non-STE: The contract defines three methods.

## INVALID (adj)  ✓

- STE: An invalid token.  |  Non-STE: A bad token.

## ISOLATE (v)  ✓

- STE: Isolate the component for unit testing.  |  Non-STE: Separate the component for unit testing.

## IT (pron)  ✓

- STE: The package. It is in the registry.  |  Non-STE: The package is in the registry.

# J

## JOIN (v)  ✓

- STE: Join the two strings.  |  Non-STE: Concatenate the two strings.

# K

## KEEP (v)  ✓

- STE: Keep the connection open.  |  Non-STE: Maintain the connection.

## KEY (n)  ✓

- STE: The key for the cache entry is the user ID.  |  Non-STE: The identifier for the cache entry is the user ID.

## KILL (v)  ✓

- STE: Kill the process with SIGTERM.  |  Non-STE: Terminate the process with SIGTERM.

## KNOW (v)  ✓

- STE: You must know the API specification.  |  Non-STE: You must be familiar with the API specification.

# L

## LARGE (adj)  ✓

- STE: A large dataset.  |  Non-STE: A big dataset.

## LAST (adj)  ✓

- STE: Execute the teardown last.  |  Non-STE: Execute the teardown at the end.

## LAYER (n)  ✓

- STE: The data access layer handles queries.  |  Non-STE: The data tier handles queries.

## LEFT (adj)  ✓

- STE: Align the text left.  |  Non-STE: Align the text to the left.

## LENGTH (n)  ✓

- STE: The length of the array is 10.  |  Non-STE: The array has 10 elements.

## LESS (adj)  ✓

- STE: Less memory usage.  |  Non-STE: Lower memory usage.

## LET (v)  ✓

- STE: Let the process complete before you restart.  |  Non-STE: Allow the process to complete before you restart.

## LEVEL (n)  ✓

- STE: Set the log level to debug.  |  Non-STE: Set the logging severity to debug.

## LIBRARY (n)  ✓

- STE: Import the standard library.  |  Non-STE: Include the standard library.

## LIFT (v)  ✓

- STE: Lift the function to a separate module.  |  Non-STE: Extract the function to a separate module.

## LIGHT (adj)  ✓

- STE: A light process with small memory footprint.  |  Non-STE: A lightweight process.

## LIMIT (n)  ✓

- STE: Limit the number of requests.  |  Non-STE: Restrict the number of requests.

## LINE (n)  ✓

- STE: The error is at line 42.  |  Non-STE: The error is on line 42.

## LINK (n)  ✓

- STE: Link the library to the project.  |  Non-STE: Connect the library to the project.

## LIST (n)  ✓

- STE: List the files in the directory.  |  Non-STE: Show the files in the directory.

## LOAD (n)  ✓

- STE: Load the configuration file.  |  Non-STE: Read the configuration file.

## LOCATE (v)  ✗

Not approved. Use the STE form below.
- STE: Find the error in the logs.  |  Non-STE: Locate the error in the logs.

## LOCK (v)  ✓

- STE: Lock the mutex.  |  Non-STE: Acquire the mutex.

## LOG (n)  ✓

- STE: Log the error to the file.  |  Non-STE: Write the error to the file.

## LONG (adj)  ✓

- STE: A long process.  |  Non-STE: A time-consuming process.

## LOOK (v)  ✓

- STE: Look at the error message.  |  Non-STE: Examine the error message.

## LOOP (n)  ✓

- STE: The for loop iterates 10 times.  |  Non-STE: The iteration runs 10 times.

## LOOSE (adj)  ✓

- STE: Loose coupling between modules.  |  Non-STE: Decoupled modules.

## LOW (adj)  ✓

- STE: Low latency.  |  Non-STE: Minimal delay.

## LOWER (v)  ✓

- STE: Lower the log level.  |  Non-STE: Reduce the log level.

# M

## MAIN (adj)  ✗

Not approved. Use the STE form below.
- STE: The primary cause of the crash is a null pointer.  |  Non-STE: The main cause of the crash is a null pointer.

## MAKE (v)  ✓

- STE: Make a copy of the file.  |  Non-STE: Create a copy of the file.

## MAKE  ✓

- STE: Make sure that the tests pass.  |  Non-STE: Ensure that the tests pass.

## MANAGE (v)  ✓

- STE: The package manager manages dependencies.  |  Non-STE: The package manager handles dependencies.

## MANDATORY (adj)  ✓

- STE: The API key is mandatory.  |  Non-STE: The API key is required.

## MANUAL (adj)  ✓

- STE: Manual review of the code.  |  Non-STE: Human review of the code.
- STE: Read the manual before you start.  |  Non-STE: Read the docs before you start.

## MANY (adj)  ✓

- STE: Many requests per second.  |  Non-STE: Numerous requests per second.

## MAP (v)  ✓

- STE: Map the array to uppercase.  |  Non-STE: Transform each element of the array.

## MARK (n)  ✓

- STE: Mark the function as deprecated.  |  Non-STE: Flag the function as deprecated.

## MATCH (v)  ✓

- STE: The pattern must match the input.  |  Non-STE: The pattern must correspond to the input.

## MATERIAL (n)  ✓

- STE: Refer to the training material.  |  Non-STE: Refer to the training resources.

## MAXIMUM (adj)  ✓

- STE: Maximum connections is 100.  |  Non-STE: The limit is 100 connections.

## MEASURE (v)  ✓

- STE: Measure the response time.  |  Non-STE: Calculate the response time.

## MEMORY (n)  ✓

- STE: The application uses 256 MB of memory.  |  Non-STE: The application uses 256 MB of RAM.

## MERGE (v)  ✓

- STE: Merge the feature branch into main.  |  Non-STE: Combine the feature branch into main.

## MESSAGE (n)  ✓

- STE: The error message describes the issue.  |  Non-STE: The error text describes the issue.

## METHOD (n)  ✓

- STE: The method takes two parameters.  |  Non-STE: The function takes two parameters.

## MINIMUM (adj)  ✓

- STE: The minimum password length is 8.  |  Non-STE: The password must be at least 8 characters.

## MINUS (prep)  ✓

- STE: The value is total minus overhead.  |  Non-STE: The value is total less overhead.

## MISSING (adj)  ✓

- STE: A missing dependency.  |  Non-STE: A dependency that is not installed.

## MIX (v)  ✓

- STE: Do not mix concerns in a single module.  |  Non-STE: Do not combine concerns in a single module.

## MODE (n)  ✓

- STE: The debug mode shows more information.  |  Non-STE: Debug builds show more information.

## MODEL (n)  ✓

- STE: The user model has three fields.  |  Non-STE: The user schema has three fields.

## MODIFY (v)  ✗

Not approved. Use the STE form below.
- STE: Change the file permissions.  |  Non-STE: Modify the file permissions.

## MODULE (n)  ✓

- STE: Each module has its own namespace.  |  Non-STE: Each package has its own namespace.

## MONITOR (v)  ✓

- STE: Monitor the server logs.  |  Non-STE: Watch the server logs.

## MORE (adj)  ✓

- STE: More memory allocation.  |  Non-STE: Additional memory allocation.

## MOST (adj)  ✓

- STE: Most errors occur at startup.  |  Non-STE: The majority of errors occur at startup.

## MOVE (v)  ✓

- STE: Move the file to the archive.  |  Non-STE: Transfer the file to the archive.

## MUCH (adj)  ✓

- STE: Not much memory usage.  |  Non-STE: Low memory usage.

## MUST (v)  ✓

- STE: You must validate all inputs.  |  Non-STE: You have to validate all inputs.

# N

## NAME (n)  ✓

- STE: Name the variable `count`.  |  Non-STE: Call the variable `count`.

## NEAR (adj)  ✓

- STE: Near the end of the file.  |  Non-STE: Close to the end of the file.

## NECESSARY (adj)  ✓

- STE: It is necessary to restart the service.  |  Non-STE: You must restart the service.

## NEED (v)  ✗

Not approved. Use the STE form below.
- STE: You must install the dependencies.  |  Non-STE: You need to install the dependencies.

## NEVER (adv)  ✓

- STE: Never store passwords in plain text.  |  Non-STE: Do not store passwords in plain text under any circumstances.

## NEW (adj)  ✓

- STE: A new instance of the class.  |  Non-STE: A fresh instance of the class.

## NEXT (adj)  ✓

- STE: The next iteration.  |  Non-STE: The following iteration.

## NO (adj)  ✓

- STE: No errors in the output.  |  Non-STE: Zero errors in the output.

## NONE (pron)  ✓

- STE: None of the tests fail.  |  Non-STE: All tests pass.

## NORMAL (adj)  ✗

Not approved. Use the STE form below.
- STE: The usual behavior is to return zero.  |  Non-STE: The normal behavior is to return zero.

## NOT (adv)  ✓

- STE: Do not use deprecated functions.  |  Non-STE: Avoid using deprecated functions.

## NOTE (n)  ✓

- STE: Add a note in the code.  |  Non-STE: Add a comment in the code.

## NULL (adj)  ✓

- STE: The pointer is null.  |  Non-STE: The pointer is empty.

## NUMBER (n)  ✓

- STE: The number of records is 100.  |  Non-STE: The count of records is 100.

# O

## OBJECT (n)  ✓

- STE: Create a new object of the User class.  |  Non-STE: Instantiate the User class.

## OBEY (v)  ✓

- STE: Obey the coding standards.  |  Non-STE: Follow the coding standards.

## OCCUR (v)  ✓

- STE: An exception occurred at runtime.  |  Non-STE: An exception was thrown at runtime.

## OF (prep)  ✓

- STE: The name of the function.  |  Non-STE: The function's name.

## OFF (adv)  ✓

- STE: Turn off the feature flag.  |  Non-STE: Disable the feature flag.

## ON (adv)  ✓

- STE: Turn on the debug mode.  |  Non-STE: Enable the debug mode.

## ONLY (adv)  ✓

- STE: Only the admin can run this command.  |  Non-STE: Solely the admin can run this command.

## OPEN (v)  ✓

- STE: Open the file for reading.  |  Non-STE: Read the file.
- STE: An open port on the firewall.  |  Non-STE: A listening port on the firewall.

## OPERATE (v)  ✓

- STE: Operate the application through the CLI.  |  Non-STE: Run the application through the CLI.

## OPERATION (n)  ✓

- STE: The operation of the request is asynchronous.  |  Non-STE: The request is processed asynchronously.

## OPTION (n)  ✗

Not approved. Use the STE form below.
- STE: You can use an alternative configuration.  |  Non-STE: You have the option to use another configuration.

## OR (conj)  ✓

- STE: Use Python or Node.js.  |  Non-STE: Use Python; alternatively use Node.js.

## ORDER (n)  ✓

- STE: Execute the steps in the given order.  |  Non-STE: Execute the steps sequentially.

## OTHER (adj)  ✓

- STE: The other endpoint returns JSON.  |  Non-STE: The alternative endpoint returns JSON.

## OUTPUT (n)  ✓

- STE: The output of the command is a list.  |  Non-STE: The command prints a list.

## OVER (prep)  ✗

Not approved. Use the STE form below.
- STE: More than the threshold.  |  Non-STE: Over the threshold.

## OVERRIDE (v)  ✓

- STE: Override the default behavior in the subclass.  |  Non-STE: Replace the default behavior in the subclass.

# P

## PACKAGE (n)  ✓

- STE: Install the package with pip.  |  Non-STE: Install the library with pip.

## PAGE (n)  ✓

- STE: The landing page of the application.  |  Non-STE: The home screen of the application.

## PARAMETER (n)  ✓

- STE: The function takes two parameters.  |  Non-STE: The function accepts two arguments.

## PART (n)  ✓

- STE: A part of the documentation.  |  Non-STE: A section of the documentation.

## PASS (v)  ✓

- STE: The test passes.  |  Non-STE: The test succeeds.

## PASTE (v)  ✓

- STE: Paste the text into the editor.  |  Non-STE: Insert the copied text into the editor.

## PATH (n)  ✓

- STE: The path to the config file is `/etc/app/`.  |  Non-STE: The location of the config file is `/etc/app/`.

## PATTERN (n)  ✓

- STE: The regex pattern matches the input.  |  Non-STE: The regular expression matches the input.

## PERFORM (v)  ✗

Not approved. Use the STE form below.
- STE: Do the build.  |  Non-STE: Perform the build.

## PERFORMANCE (n)  ✓

- STE: The performance of the query is good.  |  Non-STE: The query runs fast.

## PERMANENT (adj)  ✓

- STE: Write the data to permanent storage.  |  Non-STE: Write the data to persistent storage.

## PERMIT (v)  ✗

Not approved. Use the STE form below.
- STE: The API lets you send 100 requests per minute.  |  Non-STE: The API permits 100 requests per minute.

## PERSON (n)  ✓

- STE: Only one person can access the account.  |  Non-STE: Only a single user can access the account.

## PIPE (n)  ✓

- STE: Use a pipe to connect the commands.  |  Non-STE: Use the pipe operator to connect the commands.

## PLACE (n)  ✓

- STE: Place the hook in the lifecycle at the right position.  |  Non-STE: Insert the hook into the lifecycle.

## PLUS (prep)  ✓

- STE: The total is the base plus the overhead.  |  Non-STE: The total is the sum of the base and overhead.

## POINT (n)  ✓

- STE: The entry point of the application is `main()`.  |  Non-STE: The application starts at `main()`.

## PORT (n)  ✓

- STE: The application listens on port 8080.  |  Non-STE: The application uses port 8080.

## POSITION (n)  ✓

- STE: The position of the element in the array is 0.  |  Non-STE: The index of the element in the array is 0.

## POSSIBLE (adj)  ✓

- STE: A possible solution is to increase the timeout.  |  Non-STE: One solution could be to increase the timeout.

## POWER (n)  ✓

- STE: The processing power of the server is sufficient.  |  Non-STE: The server has enough CPU.

## PREPARE (v)  ✓

- STE: Prepare the environment for deployment.  |  Non-STE: Set up the environment for deployment.

## PREVENT (v)  ✓

- STE: Use parameterized queries to prevent SQL injection.  |  Non-STE: Use parameterized queries to avoid SQL injection.

## PREVIOUS (adj)  ✓

- STE: The previous version had a bug.  |  Non-STE: The prior version had a bug.

## PRIMARY (adj)  ✓

- STE: The primary key of the table is the `id` field.  |  Non-STE: The main key of the table is the `id` field.

## PROBLEM (n)  ✓

- STE: Identify the root cause of the problem.  |  Non-STE: Find what caused the issue.

## PROCEDURE (n)  ✓

- STE: Do the deployment procedure.  |  Non-STE: Follow the deployment procedure.

## PROCESS (n)  ✗

Not approved. Use the STE form below.
- STE: Process the request synchronously.  |  Non-STE: Handle the request synchronously.

## PROVIDE (v)  ✗

Not approved. Use the STE form below.
- STE: The function returns the result.  |  Non-STE: The function provides the result.

## PULL (v)  ✓

- STE: Pull the latest changes from the repository.  |  Non-STE: Fetch the latest changes from the repository.

## PUSH (v)  ✓

- STE: Push the commit to the remote.  |  Non-STE: Upload the commit to the remote.

## PUT (v)  ✓

- STE: Put the value in the variable.  |  Non-STE: Assign the value to the variable.

# Q

## QUALITY (n)  ✓

- STE: Code quality is important.  |  Non-STE: The standard of the code is important.

## QUANTITY (n)  ✓

- STE: A large quantity of data.  |  Non-STE: A lot of data.

## QUERY (n)  ✓

- STE: The query returns 10 rows.  |  Non-STE: The SQL statement returns 10 rows.

## QUICK (adj)  ✓

- STE: Process the request quickly.  |  Non-STE: Process the request fast.

# R

## RAISE (v)  ✓

- STE: Raise an exception when the value is null.  |  Non-STE: Throw an exception when the value is null.

## RANGE (n)  ✓

- STE: The port range is 8000-8080.  |  Non-STE: The ports go from 8000 to 8080.

## READ (v)  ✓

- STE: Read the file from disk.  |  Non-STE: Load the file from disk.

## READY (adj)  ✓

- STE: The build is ready for deployment.  |  Non-STE: The build can be deployed.

## RECEIVE (v)  ✓

- STE: Receive the HTTP response.  |  Non-STE: Get the HTTP response.

## RECOMMEND (v)  ✓

- STE: The style guide recommends this format.  |  Non-STE: The style guide suggests this format.

## RECORD (v)  ✓

- STE: Record the error in the log.  |  Non-STE: Log the error.

## REDUCE (v)  ✗

Not approved. Use the STE form below.
- STE: Decrease the memory usage.  |  Non-STE: Reduce the memory usage.

## REFER (v)  ✓

- STE: Refer to the API documentation for details.  |  Non-STE: See the API documentation for details.

## REFRESH (v)  ✓

- STE: Refresh the page to see the changes.  |  Non-STE: Reload the page to see the changes.

## REJECT (v)  ✓

- STE: Reject the commit if tests fail.  |  Non-STE: Deny the commit if tests fail.

## RELEASE (v)  ✓

- STE: Release the new version to production.  |  Non-STE: Publish the new version to production.
- STE: Release the memory after use.  |  Non-STE: Free the memory after use.

## REMAINING (adj)  ✓

- STE: Fix the remaining warnings.  |  Non-STE: Fix the leftover warnings.

## REMOVE (v)  ✓

- STE: Remove the deprecated function.  |  Non-STE: Delete the deprecated function.

## REPAIR (v)  ✓

- STE: Repair the broken build.  |  Non-STE: Fix the broken build.

## REPEAT (v)  ✓

- STE: Repeat the operation for each item.  |  Non-STE: Loop through the items and do the operation.

## REPLACE (v)  ✓

- STE: Replace the old library with the new one.  |  Non-STE: Swap the old library for the new one.

## REPORT (n)  ✓

- STE: Report the bug in the issue tracker.  |  Non-STE: Log the bug in the issue tracker.

## REQUEST (n)  ✓

- STE: The HTTP request returns 200 OK.  |  Non-STE: The HTTP call returns 200 OK.

## REQUIRE (v)  ✗

Not approved. Use the STE form below.
- STE: You must install Node.js.  |  Non-STE: The project requires Node.js.

## RESOURCE (n)  ✓

- STE: Free the resources after use.  |  Non-STE: Release the resources after use.

## RESPONSE (n)  ✓

- STE: The response contains the user data.  |  Non-STE: The reply contains the user data.

## RESTART (v)  ✓

- STE: Restart the service.  |  Non-STE: Stop and start the service.

## RESULT (n)  ✓

- STE: The result of the query is an empty set.  |  Non-STE: The query returns no rows.

## RETRY (v)  ✓

- STE: Retry the request after 5 seconds.  |  Non-STE: Try the request again after 5 seconds.

## RETURN (v)  ✓

- STE: The function returns the computed value.  |  Non-STE: The function gives back the computed value.

## REVIEW (n)  ✗

Not approved. Use the STE form below.
- STE: Examine the code for issues.  |  Non-STE: Review the code for issues.

## RIGHT (adj)  ✓

- STE: Align the text right.  |  Non-STE: Align the text to the right.

## RISK (n)  ✓

- STE: The risk of data loss is small.  |  Non-STE: There is little chance of data loss.

## ROOT (n)  ✓

- STE: The config file is in the root of the project.  |  Non-STE: The config file is at the top level of the project.
- STE: Run the command as root.  |  Non-STE: Run the command with superuser privileges.

## ROUTE (n)  ✓

- STE: The route `/users` returns the user list.  |  Non-STE: The endpoint `/users` returns the user list.

## RULE (n)  ✓

- STE: The validation rule checks the email format.  |  Non-STE: The validation checks the email format.

## RUN (v)  ✓

- STE: Run the script from the terminal.  |  Non-STE: Execute the script from the terminal.

# S

## SAFE (adj)  ✓

- STE: A safe default value prevents crashes.  |  Non-STE: A sensible default value prevents crashes.
- STE: For data safety, encrypt the backup.  |  Non-STE: For security, encrypt the backup.

## SAME (adj)  ✓

- STE: The two functions return the same result.  |  Non-STE: The two functions return identical results.

## SAMPLE (n)  ✓

- STE: A code sample is in the `examples/` directory.  |  Non-STE: An example is in the `examples/` directory.

## SAVE (v)  ✓

- STE: Save the file to disk.  |  Non-STE: Write the file to disk.

## SCHEDULE (v)  ✓

- STE: Schedule the job to run daily.  |  Non-STE: Set the job to run daily.

## SEARCH (v)  ✓

- STE: Search the logs for error messages.  |  Non-STE: Look through the logs for error messages.

## SECTION (n)  ✓

- STE: Refer to the Security section of the README.  |  Non-STE: See the Security part of the README.

## SEE (v)  ✓

- STE: See the documentation for details.  |  Non-STE: Refer to the documentation for details.

## SELECT (v)  ✓

- STE: Select the database from the list.  |  Non-STE: Choose the database from the list.

## SEND (v)  ✓

- STE: Send the request to the server.  |  Non-STE: Make the request to the server.

## SEPARATE (adj)  ✗

Not approved. Use the STE form below.
- STE: Keep the modules isolated from each other.  |  Non-STE: Keep the modules separate from each other.

## SEQUENCE (n)  ✓

- STE: Execute the steps in the given sequence.  |  Non-STE: Execute the steps in order.

## SERVER (n)  ✓

- STE: The server listens on port 443.  |  Non-STE: The service listens on port 443.

## SERVICE (n)  ✓

- STE: The authentication service is down.  |  Non-STE: The auth service is not running.

## SET (n)  ✓

- STE: Set the variable to 10.  |  Non-STE: Assign 10 to the variable.

## SHORT (adj)  ✓

- STE: A short timeout of 1 second.  |  Non-STE: A brief timeout of 1 second.

## SHOW (v)  ✓

- STE: The command shows the file contents.  |  Non-STE: The command displays the file contents.

## SHUT  ✗

Not approved. Use the STE form below.
- STE: Stop the server.  |  Non-STE: Shut down the server.

## SIGNAL (n)  ✓

- STE: Send a SIGTERM signal to the process.  |  Non-STE: Terminate the process.

## SIMPLE (adj)  ✓

- STE: A simple function with one responsibility.  |  Non-STE: A straightforward function with one responsibility.

## SINGLE (adj)  ✓

- STE: A single instance of the application.  |  Non-STE: One instance of the application.

## SIZE (n)  ✓

- STE: The size of the file is 2 MB.  |  Non-STE: The file is 2 MB.

## SLOW (adj)  ✓

- STE: Slowly increase the timeout value.  |  Non-STE: Gradually increase the timeout value.

## SMALL (adj)  ✓

- STE: A small amount of memory is allocated.  |  Non-STE: A negligible amount of memory is allocated.

## SOCKET (n)  ✓

- STE: Open a socket on port 3000.  |  Non-STE: Create a connection on port 3000.

## SOLUTION (n)  ✓

- STE: The solution to the memory leak is to use weak references.  |  Non-STE: Fix the memory leak by using weak references.

## SOME (adj)  ✓

- STE: Some tests fail under load.  |  Non-STE: A few tests fail under load.

## SOURCE (n)  ✓

- STE: Find the source of the bug.  |  Non-STE: Locate where the bug originates.

## SPACE (n)  ✓

- STE: Make sure that there is sufficient disk space.  |  Non-STE: Check that there is enough disk space.

## SPECIAL (adj)  ✓

- STE: Use the special config for staging.  |  Non-STE: Use the staging-specific config.

## SPECIFIED (adj)  ✓

- STE: Use the specified port number from the config.  |  Non-STE: Use the port number that is given in the config.

## SPEED (n)  ✓

- STE: The speed of the query is fast.  |  Non-STE: The query is fast.

## STACK (n)  ✓

- STE: Push the value onto the stack.  |  Non-STE: Add the value to the stack.

## STAGE (n)  ✗

Not approved. Use the STE form below.
- STE: During this step, do not merge the branch.  |  Non-STE: At this stage, do not merge the branch.

## STANDARD (adj)  ✓

- STE: Follow the standard coding conventions.  |  Non-STE: Follow the usual coding conventions.

## START (n)  ✓

- STE: Start the application.  |  Non-STE: Launch the application.

## STATE (n)  ✗

Not approved. Use the STE form below.
- STE: Examine the condition of the system.  |  Non-STE: Examine the state of the system.

## STATUS (n)  ✓

- STE: The status of the service is "healthy."  |  Non-STE: The service is healthy.

## STAY (v)  ✓

- STE: Make sure that the connection stays open.  |  Non-STE: Keep the connection open.

## STEP (n)  ✓

- STE: Do steps 1 through 5 in the given order.  |  Non-STE: Follow the procedure steps 1-5.

## STOP (v)  ✓

- STE: Stop the process.  |  Non-STE: Kill the process.
- STE: When the errors stop, check the logs.  |  Non-STE: When the errors cease, check the logs.

## STORE (v)  ✗

Not approved. Use the STE form below.
- STE: Keep the config files in version control.  |  Non-STE: Store the config files in version control.

## STREAM (n)  ✓

- STE: Process the data as a stream.  |  Non-STE: Process the data in chunks.

## STRING (n)  ✓

- STE: The response returns a JSON string.  |  Non-STE: The response returns JSON text.

## STRONG (adj)  ✓

- STE: Use a strong password.  |  Non-STE: Use a secure password.

## STRUCTURE (n)  ✓

- STE: The structure of the project follows MVC.  |  Non-STE: The project layout follows MVC.

## SUFFICIENT (adj)  ✓

- STE: Make sure that there is sufficient disk space.  |  Non-STE: Make sure that there is enough disk space.

## SUDDEN (adj)  ✓

- STE: If the service fails suddenly, read the logs.  |  Non-STE: If the service fails unexpectedly, read the logs.

## SUPPLY (n)  ✓

- STE: Supply the API key as a query parameter.  |  Non-STE: Provide the API key as a query parameter.

## SURFACE (n)  ✓

- STE: The API surface of the library is small.  |  Non-STE: The public interface of the library is small.

## SYSTEM (n)  ✓

- STE: The authentication system uses JWT.  |  Non-STE: The authentication module uses JWT.

# T

## TABLE (n)  ✓

- STE: The `users` table has four columns.  |  Non-STE: The `users` database table has four columns.

## TAG (n)  ✓

- STE: Add a version tag to the commit.  |  Non-STE: Mark the commit with a version number.

## TAKE (v)  ✗

Not approved. Use the STE form below.
- STE: The query consumes 100 ms.  |  Non-STE: The query takes 100 ms.

## TASK (n)  ✓

- STE: The asynchronous task runs in the background.  |  Non-STE: The background job runs asynchronously.

## TELL (v)  ✓

- STE: The log file tells you the error location.  |  Non-STE: The log file shows you the error location.

## TEMPORARY (adj)  ✓

- STE: Create a temporary file for the intermediate data.  |  Non-STE: Create a temp file for the intermediate data.

## TERMINATE (v)  ✓

- STE: Terminate the hung process.  |  Non-STE: Kill the hung process.

## TEST (n)  ✓

- STE: Run the unit tests before you merge.  |  Non-STE: Execute the test suite before merging.

## TEST (v)  ✗

Not approved. Use the STE form below.
- STE: Do a test of the module.  |  Non-STE: Test the module.

## TEXT (n)  ✓

- STE: The response body contains plain text.  |  Non-STE: The response body is a string.

## THAN (conj)  ✓

- STE: The new version is faster than the previous version.  |  Non-STE: The new version outperforms the previous version.

## THAT (conj)  ✓

- STE: Make sure that the tests pass.  |  Non-STE: Ensure the tests pass.

## THE (art)  ✓

- STE: The function returns a value.  |  Non-STE: Function returns a value.

## THEN (adv)  ✓

- STE: Compile the code. Then, run the tests.  |  Non-STE: Compile the code and subsequently run the tests.

## THICK (adj)  ✓


## THREAD (n)  ✓

- STE: Run the task in a separate thread.  |  Non-STE: Run the task in parallel.

## THROUGH (prep)  ✓

- STE: Route the request through the proxy.  |  Non-STE: Pass the request via the proxy.

## THROW (v)  ✓

- STE: The function throws an error on invalid input.  |  Non-STE: The function raises an error on invalid input.

## THUS (adv)  ✓

- STE: The token expires. Thus, the request fails.  |  Non-STE: The token expires; therefore, the request fails.

## TIME (n)  ✓

- STE: The response time is 200 ms.  |  Non-STE: The latency is 200 ms.

## TIMEOUT (n)  ✓

- STE: Set the timeout to 30 seconds.  |  Non-STE: Configure a 30-second time limit.

## TO (prep)  ✓

- STE: Navigate to the settings page.  |  Non-STE: Go to the settings page.

## TOKEN (n)  ✓

- STE: Pass the token in the Authorization header.  |  Non-STE: Include the token in the request.

## TOO (adv)  ✓

- STE: Too many open connections.  |  Non-STE: Excessively many open connections.

## TOP (adj)  ✓

- STE: The top of the file contains the imports.  |  Non-STE: The beginning of the file contains the imports.

## TOUCH (v)  ✓

- STE: Touch the file to update its modification date.  |  Non-STE: Update the file timestamp.

## TRACK (v)  ✓

- STE: Track the changes with git.  |  Non-STE: Monitor the changes with git.

## TRAIN (v)  ✓

- STE: Train the model on the training set.  |  Non-STE: Fit the model to the training data.

## TRANSFER (v)  ✓

- STE: Transfer the file via SCP.  |  Non-STE: Copy the file via SCP.

## TRIGGER (v)  ✓

- STE: The event triggers the callback.  |  Non-STE: The event fires the callback.

## TRUE (adj)  ✗

Not approved. Use the STE form below.
- STE: The condition is true.  |  Non-STE: The condition evaluates to truth.

## TRY (v)  ✓

- STE: Try the request again.  |  Non-STE: Retry the request.

## TURN (v)  ✓

- STE: Turn on the feature flag.  |  Non-STE: Enable the feature flag.

## TYPE (n)  ✓

- STE: The type of the variable is string.  |  Non-STE: The variable is a string.

# U

## UNDER (prep)  ✗

Not approved. Use the STE form below.
- STE: Below the threshold.  |  Non-STE: Under the threshold.

## UNLOCK (v)  ✓

- STE: Unlock the mutex.  |  Non-STE: Release the mutex.

## UNSTABLE (adj)  ✓

- STE: The connection is unstable.  |  Non-STE: The connection is flaky.

## UNTIL (prep)  ✓

- STE: Retry the request until it succeeds.  |  Non-STE: Keep retrying the request while it fails.

## UNUSUAL (adj)  ✓

- STE: Watch for unusual log entries.  |  Non-STE: Watch for unexpected log entries.

## UP (adv)  ✓

- STE: Bring the service up.  |  Non-STE: Start the service.

## UPDATE (v)  ✓

- STE: Update the package to the latest version.  |  Non-STE: Upgrade the package to the latest version.

## USE (v)  ✓

- STE: Use the API to fetch data.  |  Non-STE: Utilize the API to fetch data.

## USUAL (adj)  ✓

- STE: Usually, the request returns 200 OK.  |  Non-STE: Typically, the request returns 200 OK.

# V

## VALID (adj)  ✗

Not approved. Use the STE form below.
- STE: Make sure that the input is correct.  |  Non-STE: Make sure that the input is valid.

## VALIDATE (v)  ✓

- STE: Validate the user input before processing.  |  Non-STE: Check the user input before processing.

## VALUE (n)  ✓

- STE: The value of the environment variable is "production".  |  Non-STE: The environment variable is set to "production".

## VARIABLE (n)  ✓

- STE: Declare the variable before use.  |  Non-STE: Define the variable before use.

## VERIFY (v)  ✗

Not approved. Use the STE form below.
- STE: Make sure that the signature is correct.  |  Non-STE: Verify the signature.

## VERSION (n)  ✓

- STE: The current version is 3.2.1.  |  Non-STE: The release is 3.2.1.

## VERY (adv)  ✓

- STE: Increase the value very slowly.  |  Non-STE: Increment the value in tiny steps.

## VIA (prep)  ✗

Not approved. Use the STE form below.
- STE: Authenticate through OAuth.  |  Non-STE: Authenticate via OAuth.

## VIEW (n)  ✓

- STE: The log view shows recent entries.  |  Non-STE: The log display shows recent entries.

## VISIBLE (adj)  ✗

Not approved. Use the STE form below.
- STE: Make sure that you can see the output in the terminal.  |  Non-STE: Make sure that the output is visible in the terminal.

## VISUAL (adj)  ✓

- STE: Do a visual inspection of the UI.  |  Non-STE: Visually inspect the UI.

## VOLUME (n)  ✓

- STE: Mount the volume to the container.  |  Non-STE: Attach the storage to the container.

# W

## WAIT (v)  ✓

- STE: Wait for the asynchronous task to complete.  |  Non-STE: Block until the async task finishes.

## WANT (v)  ✓

- STE: Install the package that you want.  |  Non-STE: Install the desired package.

## WARNING (n)  ✓

- STE: The compiler shows a warning for the deprecated function.  |  Non-STE: The compiler warns about the deprecated function.

## WATCH (v)  ✗

Not approved. Use the STE form below.
- STE: Monitor the log output for errors.  |  Non-STE: Watch the log output for errors.

## WE (pron)  ✓

- STE: We recommend using the latest API.  |  Non-STE: The team recommends using the latest API.

## WEAK (adj)  ✓

- STE: A weak reference does not prevent garbage collection.  |  Non-STE: A soft reference does not prevent garbage collection.

## WEIGHT (n)  ✓

- STE: The weight of the config value is 0.5.  |  Non-STE: The priority of the config value is 0.5.

## WHEN (conj)  ✓

- STE: When the build finishes, deploy the artifact.  |  Non-STE: After the build finishes, deploy the artifact.

## WHERE (conj)  ✓

- STE: Find the line where the error occurred.  |  Non-STE: Find the line at which the error occurred.

## WHILE (conj)  ✓

- STE: Log the progress while the script runs.  |  Non-STE: Log the progress as the script executes.

## WHOLE (adj)  ✗

Not approved. Use the STE form below.
- STE: Examine all of the codebase.  |  Non-STE: Examine the whole codebase.

## WIDE (adj)  ✓

- STE: Wide test coverage.  |  Non-STE: Broad test coverage.

## WILL (v)  ✓

- STE: The docs will help you to set up the project.  |  Non-STE: The docs are going to help you set up the project.

## WITH (prep)  ✓

- STE: Compare the result with the expected value.  |  Non-STE: Compare the result against the expected value.

## WITHOUT (prep)  ✓

- STE: Run the build without caching.  |  Non-STE: Run the build with caching disabled.

## WORK (n)  ✓

- STE: Do the work in a dedicated branch.  |  Non-STE: Do the task in a dedicated branch.

## WORKER (n)  ✓

- STE: The worker processes jobs from the queue.  |  Non-STE: The background job processor handles the queue.

## WRITE (v)  ✓

- STE: Write the result to a file.  |  Non-STE: Save the result to a file.

## WRONG (adj)  ✗

Not approved. Use the STE form below.
- STE: Mark the variable as private to prevent incorrect usage.  |  Non-STE: Mark the variable as private to prevent wrong usage.

# Y

## YES (adv)  ✓

- STE: Does the test pass? Yes or no?  |  Non-STE: Is the test passing? Affirmative or negative?

## YET (conj)  ✗

Not approved. Use the STE form below.
- STE: Compile the project, but skip the tests.  |  Non-STE: Compile the project, yet skip the tests.

## YET (adv)  ✗

Not approved. Use the STE form below.
- STE: Do not deploy the feature at this time.  |  Non-STE: Do not deploy the feature yet.

## YOU (pron)  ✓

- STE: You can run the script from the command line.  |  Non-STE: The user can run the script from the command line.

## YOUR (adj)  ✓

- STE: If you get an error in your terminal, read the logs.  |  Non-STE: If an error appears in the terminal, read the logs.

# Z

## ZERO (n)  ✓

- STE: Initialize the counter to zero.  |  Non-STE: Set the counter to 0.

## List  ✓


## Summary  ✓
