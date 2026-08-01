# STE-Code Adapted Dictionary A-Z

> **Source:** Adapted from ASD-STE100 Issue 9, Part 2 - Dictionary, Pages 149-434
> **Source file:** ste-code/merged/master.md (lines 5591-10976)
> **Generated:** 2026-07-30
> **Domain adaptation:** aerospace → code documentation (API docs, commit messages, README sections, code comments)
> **Preserved:** word alphabetization, STE/non-STE pair format, approved/unapproved status, parts of speech
> **Replaced:** aerospace examples with code examples
> **Approved words:** ~875 (UPPERCASE) | **Unapproved words:** ~1274 (lowercase + UNNAPROVED)

---

## How to Read This Dictionary

- **UPPERCASE words** are approved in STE-Code.
- **lowercase words** are not approved; use the listed alternatives instead.
- **(v)** = verb, **(n)** = noun, **(adj)** = adjective, **(adv)** = adverb, **(prep)** = preposition, **(conj)** = conjunction, **(pron)** = pronoun, **(art)** = article
- **(TN)** = code-domain Technical Noun, **(TV)** = code-domain Technical Verb
- Each entry shows: original rule text → code-domain rewrite → STE/non-STE code example pairs

---

# A

## A (art)
- **Original:** Function word: indefinite article. A FUEL PUMP IS INSTALLED IN ZONE 10.
- **Code-domain:** Function word: indefinite article. A CONFIG FILE IS INCLUDED IN THE ROOT DIRECTORY.
> **STE:** A config file is included in the root directory.
> **Non-STE:** Config files included in root directory.

*Ref: master.md - Dictionary entry A (art), Page 149*

---

## ABANDON (v) - UNNAPROVED
- **Original:** GO (v), STOP (v). IF THERE IS A FIRE, IMMEDIATELY GO TO A SAFE AREA. / IF THE VALUES ARE INCORRECT, STOP THE TEST PROCEDURE.
- **Code-domain:** TERMINATE (v), STOP (v). IF THE BUILD FAILS, STOP THE DEPLOYMENT PIPELINE. / IF THE VALUES ARE INCORRECT, TERMINATE THE TEST RUN.
> **STE:** If the build fails, stop the deployment pipeline.
> **Non-STE:** If the build fails, abandon the deployment pipeline.

> **STE:** If the values are incorrect, terminate the test run.
> **Non-STE:** If the values are incorrect, abandon the test procedure.

*Ref: master.md - Dictionary entry abandon (v), Page 149*

---

## ABILITY (n) - UNNAPROVED
- **Original:** CAN (v). ONE GENERATOR CAN SUPPLY POWER FOR ALL THE SYSTEMS.
- **Code-domain:** CAN (v). ONE CONFIGURATION CAN HANDLE REQUESTS FOR ALL THE ENDPOINTS.
> **STE:** One configuration can handle requests for all the endpoints.
> **Non-STE:** One configuration has the ability to handle requests for all the endpoints.

*Ref: master.md - Dictionary entry ability (n), Page 149*

---

## ABLE (adj) - UNNAPROVED
- **Original:** CAN (v). IF YOU CAN START THE ENGINE, DO THE APPLICABLE TESTS.
- **Code-domain:** CAN (v). IF YOU CAN RUN THE SCRIPT, DO THE APPLICABLE CHECKS.
> **STE:** If you can run the script, do the applicable checks.
> **Non-STE:** If you are able to run the script, do the applicable checks.

*Ref: master.md - Dictionary entry able (adj), Page 149*

---

## ABNORMAL (adj) - UNNAPROVED
- **Original:** UNUSUAL (adj), INCORRECT (adj). LISTEN FOR UNUSUAL NOISES. / IF YOU FIND AN INCORRECT QUANTITY OF AIR FROM THE VENT MAST, DO A SYSTEM TEST.
- **Code-domain:** UNUSUAL (adj), INCORRECT (adj). WATCH FOR UNUSUAL LOG ENTRIES. / IF YOU FIND AN INCORRECT VALUE IN THE OUTPUT, DO A DEBUG RUN.
> **STE:** Watch for unusual log entries.
> **Non-STE:** Watch for abnormal log entries.

> **STE:** If you find an incorrect value in the output, do a debug run.
> **Non-STE:** If you find an abnormal value in the output, do a debug run.

*Ref: master.md - Dictionary entry abnormal (adj), Page 149*

---

## ABNORMALITY (n) - UNNAPROVED
- **Original:** DEFECT (TN). EXAMINE THE SEAL FOR DEFECTS.
- **Code-domain:** BUG (TN). EXAMINE THE REPORTED STACK TRACE FOR BUGS.
> **STE:** Examine the reported stack trace for bugs.
> **Non-STE:** Examine the reported stack trace for abnormalities.

*Ref: master.md - Dictionary entry abnormality (n), Page 149*

---

## ABOUT (prep)
- **Original:** Concerned with. FOR DATA ABOUT THE LOCATION OF CIRCUIT BREAKERS, REFER TO THE WIRING LIST. For other meanings, use: APPROXIMATELY (adv), AROUND (prep).
- **Code-domain:** Concerned with. FOR DATA ABOUT THE CONFIGURATION OF THE MODULE, REFER TO THE README. For other meanings, use: APPROXIMATELY (adv), AROUND (prep).
> **STE:** For data about the configuration of the module, refer to the README.
> **Non-STE:** For data regarding the configuration of the module, refer to the README.

> **STE:** The build takes approximately 5 minutes.
> **Non-STE:** The build takes about 5 minutes.

> **STE:** This document covers topics around testing and deployment.
> **Non-STE:** This document covers topics about testing and deployment.

*Ref: master.md - Dictionary entry ABOUT (prep), Page 150*

---

## ABOVE (prep)
- **Original:** In (or to) a position farther up than something. LIFT THE CYLINDER ABOVE ITS INSTALLED POSITION. For other meanings, use: MORE THAN.
- **Code-domain:** In (or to) a position higher than something. MOVE THE CURSOR ABOVE THE TARGET LINE. For other meanings, use: MORE THAN.
> **STE:** Move the cursor above the target line.
> **Non-STE:** Move the cursor to a position above the target line.

> **STE:** The response time must be more than 200 ms.
> **Non-STE:** The response time must be above 200 ms.

*Ref: master.md - Dictionary entry ABOVE (prep), Page 150*

---

## ABRASIVE (adj) - (retained; no STE-code direct equivalent)
- **Original:** That can remove material by friction. POLISH THE SURFACE WITH AN ABRASIVE PAPER.
- **Code-domain:** Not applicable to code documentation domain. Retained for completeness but not adapted.
> **Note:** This word has no code-documentation equivalent. Use only if describing physical hardware.

*Ref: master.md - Dictionary entry ABRASIVE (adj), Page 150*

---

## ABRUPT (adj) - UNNAPROVED
- **Original:** SUDDEN (adj), SUDDENLY (adv). THE DAMPER PREVENTS SUDDEN MOVEMENT OF THE CONTROL. / IF THE ROTORS STOP SUDDENLY, EXAMINE THE INTAKE.
- **Code-domain:** SUDDEN (adj), SUDDENLY (adv). THE WATCHDOG PREVENTS SUDDEN SHUTDOWN OF THE SERVICE. / IF THE PROCESS STOPS SUDDENLY, EXAMINE THE LOGS.
> **STE:** The watchdog prevents sudden shutdown of the service.
> **Non-STE:** The watchdog prevents abrupt shutdown of the service.

> **STE:** If the process stops suddenly, examine the logs.
> **Non-STE:** If the process comes to an abrupt stop, examine the logs.

*Ref: master.md - Dictionary entry abrupt (adj), Page 150*

---

## ABSENCE (n) - UNNAPROVED
- **Original:** NONE (pron), NOT (adv), NO (adj). IF NONE OF THE BRACKETS ARE DAMAGED, CONTINUE THE PROCEDURE.
- **Code-domain:** NONE (pron), NOT (adv), NO (adj). IF NONE OF THE TESTS FAIL, CONTINUE THE DEPLOYMENT.
> **STE:** If none of the tests fail, continue the deployment.
> **Non-STE:** In the absence of test failures, continue the deployment.

> **STE:** If the tests are not failing, continue the deployment.
> **Non-STE:** In the absence of test failures, continue the deployment.

> **STE:** If there is no error in the output, continue the procedure.
> **Non-STE:** In the absence of errors in the output, continue the procedure.

*Ref: master.md - Dictionary entry absence (n), Page 151*

---

## ABSENT (adj) - UNNAPROVED
- **Original:** MISSING (adj), NO (adj). IF ONE OR MORE BLADES ARE MISSING, MAKE AN ENTRY IN THE ENGINE LOGBOOK.
- **Code-domain:** MISSING (adj), NO (adj). IF ONE OR MORE FILES ARE MISSING, ADD AN ENTRY IN THE CHANGELOG.
> **STE:** If one or more files are missing, add an entry in the changelog.
> **Non-STE:** If one or more files are absent, add an entry in the changelog.

*Ref: master.md - Dictionary entry absent (adj), Page 151*

---

## ABSOLUTELY (adv) - UNNAPROVED
- **Original:** FULLY (adv). MAKE SURE THAT THE LATCH IS FULLY ENGAGED.
- **Code-domain:** FULLY (adv). MAKE SURE THAT THE CONNECTION IS FULLY ESTABLISHED.
> **STE:** Make sure that the connection is fully established.
> **Non-STE:** Make sure that the connection is absolutely established.

*Ref: master.md - Dictionary entry absolutely (adv), Page 151*

---

## ABSORB (v)
- **Original:** 1. To take up or into. ABSORB THE FLUID WITH A CLEAN CLOTH. 2. To decrease the effect of. THE SHOCK MOUNT ABSORBS THE VIBRATION.
- **Code-domain:** 1. To take up or consume. THE BUFFER ABSORBS THE INPUT DATA. 2. To decrease the effect of. THE CACHE LAYER ABSORBS THE LOAD FROM REPEATED QUERIES.
> **STE:** The buffer absorbs the input data.
> **Non-STE:** The buffer takes up the input data.

> **STE:** The cache layer absorbs the load from repeated queries.
> **Non-STE:** The cache layer mitigates the load from repeated queries.

*Ref: master.md - Dictionary entry ABSORB (v), Page 151*

---

## ABSORPTION (n) - UNNAPROVED
- **Original:** ABSORB (v). MEASURE THE TIME THAT IS NECESSARY FOR THE SILICA GEL TO ABSORB THE MOISTURE.
- **Code-domain:** ABSORB (v). MEASURE THE TIME THAT IS NECESSARY FOR THE LOG SYSTEM TO ABSORB THE INCOMING EVENTS.
> **STE:** Measure the time that is necessary for the log system to absorb the incoming events.
> **Non-STE:** Measure the rate of absorption of incoming events by the log system.

*Ref: master.md - Dictionary entry absorption (n), Page 151*

---

## ABUNDANT (adj) - UNNAPROVED
- **Original:** LARGE (adj). CLEAN YOUR SKIN WITH A LARGE QUANTITY OF CLEAN WATER.
- **Code-domain:** LARGE (adj). LOG THE ERRORS WITH A LARGE QUANTITY OF CONTEXT DATA.
> **STE:** Log the errors with a large quantity of context data.
> **Non-STE:** Log the errors with abundant context data.

*Ref: master.md - Dictionary entry abundant (adj), Page 151*

---

## ABUT (v) - UNNAPROVED
- **Original:** TOUCH (v). THE BIN TOUCHES THE FORWARD HINGE SURFACE.
- **Code-domain:** TOUCH (v). THE WIDGET TOUCHES THE BOUNDARY OF THE CONTAINER.
> **STE:** The widget touches the boundary of the container.
> **Non-STE:** The widget abuts the boundary of the container.

*Ref: master.md - Dictionary entry abut (v), Page 152*

---

## ACCELERATE (v) - UNNAPROVED
- **Original:** INCREASE (v), FASTER (adj). A HIGHER TEMPERATURE INCREASES THE SPEED OF EVAPORATION.
- **Code-domain:** INCREASE (v), FASTER (adj). A LARGER BUFFER SIZE INCREASES THE SPEED OF DATA TRANSFER.
> **STE:** A larger buffer size increases the speed of data transfer.
> **Non-STE:** A larger buffer size accelerates data transfer.

> **STE:** To make the build process faster, use parallel compilation.
> **Non-STE:** To accelerate the build process, use parallel compilation.

*Ref: master.md - Dictionary entry accelerate (v), Page 152*

---

## ACCEPT (v)
- **Original:** To make a decision that something is satisfactory. ACCEPT THE RELAY IF IT IS SERVICEABLE.
- **Code-domain:** To make a decision that something is satisfactory. ACCEPT THE PULL REQUEST IF IT PASSES ALL CHECKS.
> **STE:** Accept the pull request if it passes all checks.
> **Non-STE:** Merge the pull request if it passes all checks.

*Ref: master.md - Dictionary entry ACCEPT (v), Page 152*

---

## ACCEPTABLE (adj) - UNNAPROVED
- **Original:** PERMITTED (adj), SATISFACTORY (adj), SERVICEABLE (adj). A VALUE OF 2 mm IS PERMITTED.
- **Code-domain:** PERMITTED (adj), SATISFACTORY (adj), READY (adj). A RESPONSE TIME OF 200 ms IS PERMITTED.
> **STE:** A response time of 200 ms is permitted.
> **Non-STE:** A response time of 200 ms is acceptable.

> **STE:** If the condition of the build is not satisfactory, run it again.
> **Non-STE:** If the condition of the build is not acceptable, run it again.

> **STE:** Before you deploy the update, make sure that it is ready.
> **Non-STE:** Before you deploy the update, make sure that it is acceptable.

*Ref: master.md - Dictionary entry acceptable (adj), Page 152*

---

## ACCEPTANCE (n) - UNNAPROVED
- **Original:** ACCEPT (v). BEFORE YOU ACCEPT THE UNIT, DO THE SPECIFIED TEST PROCEDURE.
- **Code-domain:** ACCEPT (v). BEFORE YOU ACCEPT THE MERGE REQUEST, DO THE SPECIFIED REVIEW CHECKLIST.
> **STE:** Before you accept the merge request, do the specified review checklist.
> **Non-STE:** Before acceptance of the merge request, do the specified review checklist.

*Ref: master.md - Dictionary entry acceptance (n), Page 152*

---

## ACCESS (n)
- **Original:** The ability to go into or near. GET ACCESS TO THE ACCUMULATOR FOR THE No. 1 HYDRAULIC SYSTEM.
- **Code-domain:** The ability to read, write, or enter. GET ACCESS TO THE REPOSITORY FOR THE AUTHENTICATION MODULE.
> **STE:** Get access to the repository for the authentication module.
> **Non-STE:** Access the repository for the authentication module.

*Ref: master.md - Dictionary entry ACCESS (n), Page 152*

---

## ACCESSIBLE (adj) - UNNAPROVED
- **Original:** ACCESS (n). TURN THE COVER UNTIL YOU CAN GET ACCESS TO THE JACKS THAT HAVE + AND - MARKS.
- **Code-domain:** ACCESS (n). SCROLL THE VIEW UNTIL YOU CAN GET ACCESS TO THE FUNCTIONS THAT HAVE PUBLIC ANNOTATIONS.
> **STE:** Scroll the view until you can get access to the functions that have public annotations.
> **Non-STE:** Scroll the view until the functions with public annotations are accessible.

*Ref: master.md - Dictionary entry accessible (adj), Page 152*

---

## ACCIDENT (n)
- **Original:** An occurrence that causes injury or damage. TO PREVENT ACCIDENTS, MAKE SURE THAT THE PINS ARE INSTALLED.
- **Code-domain:** An occurrence that causes harm or data loss. TO PREVENT ACCIDENTS, MAKE SURE THAT THE BACKUPS ARE INSTALLED.
> **STE:** To prevent accidents, make sure that the backups are configured.
> **Non-STE:** To prevent accidents, ensure that backups are in place.

*Ref: master.md - Dictionary entry ACCIDENT (n), Page 152*

---

## ACCIDENTAL (adj)
- **Original:** That does not occur on purpose. TO PREVENT ACCIDENTAL OPERATION OF THE SYSTEM, INSTALL THE SAFETY LOCK.
- **Code-domain:** That does not occur on purpose. TO PREVENT ACCIDENTAL DELETION OF THE FILES, CONFIRM THE OPERATION.
> **STE:** To prevent accidental deletion of the files, confirm the operation.
> **Non-STE:** To prevent inadvertent deletion of the files, confirm the operation.

*Ref: master.md - Dictionary entry ACCIDENTAL (adj), Page 153*

---

## ACCIDENTALLY (adv)
- **Original:** That does not occur on purpose. IF YOU ACCIDENTALLY MOVE THE LEVER, SET THE SYSTEM TO THE NEUTRAL POSITION AGAIN.
- **Code-domain:** That does not occur on purpose. IF YOU ACCIDENTALLY PRESS THE DELETE KEY, RESTORE THE FILE FROM THE RECYCLE BIN.
> **STE:** If you accidentally press the delete key, restore the file from the recycle bin.
> **Non-STE:** If you inadvertently press the delete key, restore the file from the recycle bin.

*Ref: master.md - Dictionary entry ACCIDENTALLY (adv), Page 153*

---

## ACCOMMODATE (v) - UNNAPROVED
- **Original:** LET (v). DIFFERENT LENGTHS OF STUDS LET YOU ATTACH DIFFERENT THICKNESSES OF SKIN.
- **Code-domain:** LET (v). DIFFERENT CONFIGURATIONS LET YOU HANDLE DIFFERENT TYPES OF INPUT.
> **STE:** Different configurations let you handle different types of input.
> **Non-STE:** Different configurations accommodate different types of input.

*Ref: master.md - Dictionary entry accommodate (v), Page 153*

---

## ACCOMPLISH (v) - UNNAPROVED
- **Original:** DO (v), COMPLETE (v). DO THIS TASK FIRST. THE PERSONNEL MUST COMPLETE THIS TASK IN 30 MINUTES.
- **Code-domain:** DO (v), COMPLETE (v). DO THIS BUILD STEP FIRST. THE PIPELINE MUST COMPLETE THIS STAGE IN 5 MINUTES.
> **STE:** Do this build step first.
> **Non-STE:** Accomplish this build step first.

> **STE:** The pipeline must complete this stage in 5 minutes.
> **Non-STE:** The pipeline must accomplish this stage in 5 minutes.

*Ref: master.md - Dictionary entry accomplish (v), Page 153*

---

## ACCORDING TO (prep) - UNNAPROVED
- **Original:** REFER (v) TO. TO CALIBRATE THE TEST SET, REFER TO THE MANUFACTURER'S INSTRUCTIONS.
- **Code-domain:** REFER (v) TO. TO CONFIGURE THE MODULE, REFER TO THE DEVELOPER'S GUIDE.
> **STE:** To configure the module, refer to the developer's guide.
> **Non-STE:** Configure the module according to the developer's guide.

*Ref: master.md - Dictionary entry according to (prep), Page 153*

---

## ACCOUNT FOR (v) - UNNAPROVED
- **Original:** MAKE SURE (v). MAKE SURE THAT YOU REMOVE ALL TOOLS AND EQUIPMENT.
- **Code-domain:** MAKE SURE (v). MAKE SURE THAT YOU TRACK ALL DEPENDENCIES AND PACKAGES.
> **STE:** Make sure that you track all dependencies and packages.
> **Non-STE:** All dependencies and packages must be accounted for.

*Ref: master.md - Dictionary entry account for (v), Page 153*

---

## ACCUMULATE (v) - UNNAPROVED
- **Original:** COLLECT (v). IF WATER COLLECTS IN THE FILLER LINE, DRAIN IT.
- **Code-domain:** COLLECT (v). IF LOGS COLLECT IN THE BUFFER, FLUSH THEM.
> **STE:** If logs collect in the buffer, flush them.
> **Non-STE:** If logs accumulate in the buffer, flush them.

*Ref: master.md - Dictionary entry accumulate (v), Page 153*

---

## ACCUMULATION (n) - UNNAPROVED
- **Original:** QUANTITY (n), COLLECT (v). REMOVE LARGE QUANTITIES OF CONTAMINATION. / IF FUEL COLLECTS FREQUENTLY, EXAMINE THE PIPE FOR LEAKS.
- **Code-domain:** QUANTITY (n), COLLECT (v). REMOVE LARGE QUANTITIES OF OBSOLETE LOGS. / IF ERRORS COLLECT FREQUENTLY, EXAMINE THE CONNECTION FOR ISSUES.
> **STE:** Remove large quantities of obsolete logs.
> **Non-STE:** Remove large accumulations of obsolete logs.

> **STE:** If errors collect frequently, examine the connection for issues.
> **Non-STE:** If accumulation of errors is frequent, examine the connection for issues.

*Ref: master.md - Dictionary entry accumulation (n), Page 153*

---

## ACCURACY (n) - UNNAPROVED
- **Original:** PRECISION (n). THE PRECISION OF THE ADJUSTMENT CAN CHANGE.
- **Code-domain:** PRECISION (n). THE PRECISION OF THE CALCULATION CAN CHANGE.
> **STE:** The precision of the calculation can change.
> **Non-STE:** The accuracy of the calculation can change.

*Ref: master.md - Dictionary entry accuracy (n), Page 154*

---

## ACCURATE (adj) - ACCURATELY (adv)
- **Original:** Exact. THE ADJUSTMENT MUST BE ACCURATE. / PUT THE REPAIR SHEET ACCURATELY ON THE DAMAGED AREA.
- **Code-domain:** Exact. THE MEASUREMENT MUST BE ACCURATE. / PUT THE PATCH ACCURATELY ON THE TARGET BRANCH.
> **STE:** The measurement must be accurate.
> **Non-STE:** The measurement must be precise.

> **STE:** Apply the patch accurately on the target branch.
> **Non-STE:** Put the patch accurately on the target branch.

*Ref: master.md - Dictionary entry ACCURATE (adj), Page 154*

---

## ACHIEVE (v) - UNNAPROVED
- **Original:** GET (v). SET THE CONTROL TO GET MAXIMUM THRUST.
- **Code-domain:** GET (v). SET THE FLAG TO GET MAXIMUM PERFORMANCE.
> **STE:** Set the flag to get maximum performance.
> **Non-STE:** Set the flag to achieve maximum performance.

*Ref: master.md - Dictionary entry achieve (v), Page 154*

---

## ACQUIRE (v) - UNNAPROVED
- **Original:** GET (v). THE COMPUTER GETS THIS DATA FROM FIVE SENSORS.
- **Code-domain:** GET (v). THE MODULE GETS THIS DATA FROM THREE ENDPOINTS.
> **STE:** The module gets this data from three endpoints.
> **Non-STE:** The module acquires this data from three endpoints.

*Ref: master.md - Dictionary entry acquire (v), Page 154*

---

## ACRID (adj) - UNNAPROVED
- **Original:** DANGEROUS (adj). THIS MATERIAL RELEASES DANGEROUS FUMES WHEN IT TOUCHES HOT SURFACES.
- **Code-domain:** Not applicable. Retained for completeness.
> **Note:** This word is domain-specific; no code-documentation equivalent.

*Ref: master.md - Dictionary entry acrid (adj), Page 154*

---

## ACROSS (prep)
- **Original:** From one side to the other side. SAFETY THE CLAMP BLOCK ACROSS THE CONTROL LEVER FORKS WITH SAFETY WIRE.
- **Code-domain:** From one file to another, spanning boundaries. SEARCH ACROSS ALL MODULES FOR THE DEPRECATED FUNCTION.
> **STE:** Search across all modules for the deprecated function.
> **Non-STE:** Search all modules for the deprecated function.

*Ref: master.md - Dictionary entry ACROSS (prep), Page 154*

---

## ACT (v) - UNNAPROVED
- **Original:** Use an accurate verb. THE HYDRAULIC FLUID FLOW OPENS THE VALVE.
- **Code-domain:** Use an accurate verb. THE EVENT TRIGGER INVOKES THE HANDLER.
> **STE:** The event trigger invokes the handler.
> **Non-STE:** The event trigger acts on the handler.

*Ref: master.md - Dictionary entry act (v), Page 154*

---

## ACTION (n) - UNNAPROVED
- **Original:** STEP (n), PROCEDURE (n), TASK (n). DO THE STEPS THAT FOLLOW.
- **Code-domain:** STEP (n), PROCEDURE (n), TASK (n). DO THE STEPS THAT FOLLOW.
> **STE:** Do the steps that follow.
> **Non-STE:** Do the following actions.

> **STE:** Do not do this procedure in the production environment.
> **Non-STE:** This action must not be done in the production environment.

> **STE:** Do this task in the staging environment.
> **Non-STE:** Do this action in the staging environment.

*Ref: master.md - Dictionary entry action (n), Page 154*

---

## ACTIVATE (v)
- **Original:** To make a system, function, or feature ready for operation. THE AUTOPILOT ACTIVATES THE APPROACH MODE. For other meanings, use: START (v).
- **Code-domain:** To make a system, function, or feature ready for operation. THE BUILD PIPELINE ACTIVATES THE DEPLOYMENT MODE. For other meanings, use: START (v).
> **STE:** The build pipeline activates the deployment mode.
> **Non-STE:** The build pipeline triggers the deployment mode.

> **STE:** Start the container.
> **Non-STE:** Activate the container.

*Ref: master.md - Dictionary entry ACTIVATE (v), Page 154*

---

## ACTIVE (adj)
- **Original:** A system, function, or feature in a state of action. DOWNLOAD THE EXPORT FILE FROM THE ACTIVE SERVER UNIT.
- **Code-domain:** A system, function, or feature in a state of action. READ THE CONFIG FROM THE ACTIVE BRANCH.
> **STE:** Read the config from the active branch.
> **Non-STE:** Read the config from the current branch.

*Ref: master.md - Dictionary entry ACTIVE (adj), Page 155*

---

## ACTIVITY (n) - UNNAPROVED
- **Original:** TASK (n), PROCEDURE (n), WORK (n). A SUBCONTRACTOR CAN DO THESE MAINTENANCE TASKS.
- **Code-domain:** TASK (n), PROCEDURE (n), WORK (n). A CONTRIBUTOR CAN DO THESE REVIEW TASKS.
> **STE:** A contributor can do these review tasks.
> **Non-STE:** A contributor can do these review activities.

> **STE:** Do this procedure in the development branch.
> **Non-STE:** Do this activity in the development branch.

> **STE:** Do this work in a clean workspace.
> **Non-STE:** Do this activity in a clean workspace.

*Ref: master.md - Dictionary entry activity (n), Page 155*

---

## ACTUATE (v) - UNNAPROVED
- **Original:** START (v), OPERATE (v), PUSH (v). START THE MOTOR. / OPERATE THE HAND PUMP. / PUSH THE PUSHBUTTON SWITCH.
- **Code-domain:** START (v), RUN (v), PUSH (v). START THE SERVER. / RUN THE SCRIPT. / PUSH THE COMMIT BUTTON.
> **STE:** Start the server.
> **Non-STE:** Actuate the server.

> **STE:** Run the script.
> **Non-STE:** Actuate the script.

*Ref: master.md - Dictionary entry actuate (v), Page 155*

---

## ACTUATION (n) - UNNAPROVED
- **Original:** OPERATION (n). MONITOR THE OPERATION OF THE STEERING MOTOR.
- **Code-domain:** OPERATION (n). MONITOR THE OPERATION OF THE BACKGROUND WORKER.
> **STE:** Monitor the operation of the background worker.
> **Non-STE:** Monitor the actuation of the background worker.

*Ref: master.md - Dictionary entry actuation (n), Page 155*

---

## ADAPT (v)
- **Original:** To change or adjust to that which is necessary. ADAPT THE PRESSURE CONNECTION TO THE PITOT HEAD. THE SYSTEM INTERFACE CIRCUITS ADAPT TO THE PHYSICAL PROPERTIES OF THE CONNECTED SYSTEMS.
- **Code-domain:** To change or adjust to that which is necessary. ADAPT THE CONNECTOR TO THE DATABASE SCHEMA. THE MIDDLEWARE LAYER ADAPTS TO THE PROTOCOL OF THE CONNECTED SERVICES.
> **STE:** Adapt the connector to the database schema.
> **Non-STE:** Adjust the connector to fit the database schema.

> **STE:** The middleware layer adapts to the protocol of the connected services.
> **Non-STE:** The middleware layer conforms to the protocol of the connected services.

*Ref: master.md - Dictionary entry ADAPT (v), Page 155*

---

## ADD (v)
- **Original:** To increase the number, dimension, or quantity. ADD 5 ml OF HARDENER TO THE COMPOUND.
- **Code-domain:** To increase the number, dimension, or quantity. ADD 5 LINES OF CONFIGURATION TO THE FILE.
> **STE:** Add 5 lines of configuration to the file.
> **Non-STE:** Append 5 lines of configuration to the file.

*Ref: master.md - Dictionary entry ADD (v), Page 155*

---

## ADDITION (n) - UNNAPROVED
- **Original:** ADD (v). TO GET THE CORRECT CLEARANCE, ADD SPECIAL SHIMS, AS NECESSARY.
- **Code-domain:** ADD (v). TO GET THE CORRECT BEHAVIOR, ADD SPECIAL FLAGS, AS NECESSARY.
> **STE:** To get the correct behavior, add special flags, as necessary.
> **Non-STE:** To get the correct behavior through the addition of special flags, as necessary.

*Ref: master.md - Dictionary entry addition (n), Page 155*

---

## ADDITIONAL (adj) - UNNAPROVED
- **Original:** MORE (adj). THIS CHAPTER GIVES MORE INFORMATION ABOUT SAFETY.
- **Code-domain:** MORE (adj). THIS SECTION GIVES MORE INFORMATION ABOUT DEPLOYMENT.
> **STE:** This section gives more information about deployment.
> **Non-STE:** This section gives additional information about deployment.

*Ref: master.md - Dictionary entry additional (adj), Page 156*

---

## ADEQUATE (adj) - UNNAPROVED
- **Original:** SUFFICIENT (adj). MAKE SURE THAT CONTAINERS HAVE SUFFICIENT CAPACITY AND DIAMETER.
- **Code-domain:** SUFFICIENT (adj). MAKE SURE THAT BUFFERS HAVE SUFFICIENT CAPACITY AND THROUGHPUT.
> **STE:** Make sure that buffers have sufficient capacity and throughput.
> **Non-STE:** Make sure that buffers have adequate capacity and throughput.

*Ref: master.md - Dictionary entry adequate (adj), Page 156*

---

## ADHERE (v) - UNNAPROVED
- **Original:** BOND (v), OBEY (v). THE SEAL MUST BOND CORRECTLY. / OBEY THE SAFETY INSTRUCTIONS.
- **Code-domain:** ATTACH (v), OBEY (v). THE PATCH MUST ATTACH CORRECTLY. / OBEY THE CODING STANDARDS.
> **STE:** The patch must attach correctly.
> **Non-STE:** The patch must adhere correctly.

> **STE:** Obey the coding standards.
> **Non-STE:** Adhere to the coding standards.

*Ref: master.md - Dictionary entry adhere (v), Page 156*

---

## ADHESION (n) - UNNAPROVED
- **Original:** BOND (n). CLEAN THE SURFACE TO MAKE SURE THAT THE BOND IS SATISFACTORY.
- **Code-domain:** Not applicable. Retained for completeness.
> **Note:** This word is domain-specific; no code-documentation equivalent.

*Ref: master.md - Dictionary entry adhesion (n), Page 156*

---

## ADJACENT (adj) - ADJACENT TO (prep)
- **Original:** That which is near to an object, with no other object of the same type between the two. DO NOT OPERATE THE ADJACENT CONTROL. / THE FUEL PUMP IS INSTALLED ADJACENT TO THE BULKHEAD.
- **Code-domain:** That which is near to an element, with no other element of the same type between the two. DO NOT MODIFY THE ADJACENT FUNCTION. / THE CONFIG FILE IS LOCATED ADJACENT TO THE MAIN MODULE.
> **STE:** Do not modify the adjacent function.
> **Non-STE:** Do not modify the function that is next to it.

> **STE:** The config file is located adjacent to the main module.
> **Non-STE:** The config file is located next to the main module.

*Ref: master.md - Dictionary entry ADJACENT (adj), Page 156*

---

## ADJOINING (adj) - UNNAPROVED
- **Original:** ADJACENT (adj). ALIGN THE BRACKETS WITH THE ADJACENT COMPONENTS.
- **Code-domain:** ADJACENT (adj). ALIGN THE IMPORTS WITH THE ADJACENT MODULES.
> **STE:** Align the imports with the adjacent modules.
> **Non-STE:** Align the imports with the adjoining modules.

*Ref: master.md - Dictionary entry adjoining (adj), Page 156*

---

## ADJUST (v)
- **Original:** To put in or come to a specified position or value. ADJUST THE FREQUENCY TO THE VALUE GIVEN IN TABLE 1. THE INTERNAL LOGIC ADJUSTS TO SUDDEN CHANGES IN TEMPERATURE.
- **Code-domain:** To put in or come to a specified position or value. ADJUST THE TIMEOUT TO THE VALUE GIVEN IN TABLE 1. THE AUTO-SCALER ADJUSTS TO SUDDEN CHANGES IN LOAD.
> **STE:** Adjust the timeout to the value given in Table 1.
> **Non-STE:** Tune the timeout to the value given in Table 1.

> **STE:** The auto-scaler adjusts to sudden changes in load.
> **Non-STE:** The auto-scaler adapts to sudden changes in load.

*Ref: master.md - Dictionary entry ADJUST (v), Page 156*

---

## ADJUSTABLE (adj) - ADJUSTMENT (n)
- **Original:** That you can adjust. THE TWO STOP BOLTS ARE ADJUSTABLE. / The effect of adjusting. MAKE SURE THAT THE ADJUSTMENT IS IN THE LIMITS GIVEN IN TABLE 1.
- **Code-domain:** That you can adjust. THE TWO PARAMETERS ARE ADJUSTABLE. / The effect of adjusting. MAKE SURE THAT THE ADJUSTMENT IS IN THE LIMITS GIVEN IN TABLE 1.
> **STE:** The two parameters are adjustable.
> **Non-STE:** The two parameters can be tuned.

> **STE:** Make sure that the adjustment is in the limits given in Table 1.
> **Non-STE:** Make sure that the tuning is in the limits given in Table 1.

*Ref: master.md - Dictionary entry ADJUSTABLE (adj), Page 156*

---

## ADMIT (v) - UNNAPROVED
- **Original:** LET (v). OPEN THE VALVE TO LET NITROGEN GO INTO THE OLEO STRUT.
- **Code-domain:** LET (v). OPEN THE PORT TO LET TRAFFIC GO INTO THE CONTAINER.
> **STE:** Open the port to let traffic go into the container.
> **Non-STE:** Open the port to admit traffic into the container.

*Ref: master.md - Dictionary entry admit (v), Page 157*

---

## ADOPT (v) - UNNAPROVED
- **Original:** USE (v). IF THE UNIT IS DAMAGED, USE THIS PROCEDURE.
- **Code-domain:** USE (v). IF THE BUILD FAILS, USE THIS FALLBACK SCRIPT.
> **STE:** If the build fails, use this fallback script.
> **Non-STE:** Adopt this fallback script if the build fails.

*Ref: master.md - Dictionary entry adopt (v), Page 157*

---

## ADVANCE (n) - UNNAPROVED
- **Original:** FORWARD (adj). THE FORWARD MOVEMENT OF THE CONTROL LEVER MUST BE SLOW AND CONTINUOUS.
- **Code-domain:** FORWARD (adj). THE FORWARD MOVEMENT OF THE ITERATOR MUST BE SEQUENTIAL.
> **STE:** The forward movement of the iterator must be sequential.
> **Non-STE:** The advance of the iterator must be sequential.

*Ref: master.md - Dictionary entry advance (n), Page 157*

---

## ADVANCE (v) - UNNAPROVED
- **Original:** SET (v), FORWARD (adv). SET THE THROTTLE TO MAXIMUM POWER. / MOVE THE LEVER FORWARD.
- **Code-domain:** SET (v), FORWARD (adv). SET THE POINTER TO THE NEXT NODE. / MOVE THE CURSOR FORWARD.
> **STE:** Set the pointer to the next node.
> **Non-STE:** Advance the pointer to the next node.

> **STE:** Move the cursor forward.
> **Non-STE:** Advance the cursor.

*Ref: master.md - Dictionary entry advance (v), Page 157*

---

## ADVERSE (adj) - UNNAPROVED
- **Original:** BAD (adj). REFER TO CHAPTER 6 FOR INSTRUCTIONS ABOUT HOW TO PARK IN BAD WEATHER CONDITIONS. If it is possible, give accurate and correct conditions. THIS MEDICATION CAN CAUSE DERMATITIS.
- **Code-domain:** BAD (adj). REFER TO SECTION 6 FOR INSTRUCTIONS ABOUT HOW TO HANDLE BAD NETWORK CONDITIONS. If it is possible, give accurate and correct conditions.
> **STE:** Refer to Section 6 for instructions about how to handle bad network conditions.
> **Non-STE:** Refer to Section 6 for instructions about how to handle adverse network conditions.

*Ref: master.md - Dictionary entry adverse (adj), Page 157*

---

## ADVISABLE (adj) - UNNAPROVED
- **Original:** RECOMMEND (v). THE DESIGN AUTHORITY RECOMMENDS THAT YOU TORQUE THE BOLTS AGAIN AT INTERVALS OF SIX MONTHS.
- **Code-domain:** RECOMMEND (v). THE TECHNICAL LEAD RECOMMENDS THAT YOU REBUILD THE CONTAINERS AT INTERVALS OF TWO WEEKS.
> **STE:** The technical lead recommends that you rebuild the containers at intervals of two weeks.
> **Non-STE:** It is advisable to rebuild the containers at intervals of two weeks.

*Ref: master.md - Dictionary entry advisable (adj), Page 157*

---

## ADVISE (v) - UNNAPROVED
- **Original:** TELL (v), RECOMMEND (v). TELL THE RAMP AGENT THAT THE BRAKES ARE SET. / THE SAFETY OFFICER RECOMMENDS THE APPLICABLE PERSONAL PROTECTIVE EQUIPMENT.
- **Code-domain:** TELL (v), RECOMMEND (v). TELL THE REVIEWER THAT THE CHANGES ARE READY. / THE SECURITY OFFICER RECOMMENDS THE APPLICABLE AUTHENTICATION PROTOCOL.
> **STE:** Tell the reviewer that the changes are ready.
> **Non-STE:** Advise the reviewer that the changes are ready.

> **STE:** The security officer recommends the applicable authentication protocol.
> **Non-STE:** The security officer advises on the applicable authentication protocol.

*Ref: master.md - Dictionary entry advise (v), Page 157*

---

## AFFECT (v) - UNNAPROVED
- **Original:** EFFECT (n). MAGNETIC TOOLS HAVE AN UNWANTED EFFECT ON THE COMPASS SYSTEM. If it is possible, be accurate. THIS MEDICATION CAN CAUSE DERMATITIS.
- **Code-domain:** EFFECT (n). THREAD LOCKS HAVE AN UNWANTED EFFECT ON THE SCHEDULER. If it is possible, be accurate.
> **STE:** Thread locks have an unwanted effect on the scheduler.
> **Non-STE:** Thread locks affect the scheduler.

*Ref: master.md - Dictionary entry affect (v), Page 158*

---

## AFT (adj), AFT (adv)
- **Original:** At or nearer to the rear of an air or sea vehicle. THE PUMP IS IN THE AFT CELL OF THE FUSELAGE TANK. / MOVE THE THROTTLE AFT.
- **Code-domain:** Not applicable to code documentation. Retained for completeness.
> **Note:** Domain-specific aerospace term; no code-documentation equivalent.

*Ref: master.md - Dictionary entry AFT (adj), Page 158*

---

## AFTER (conj)
- **Original:** That follows a specified time, sequence, or operation. AFTER YOU INSTALL THE COMPONENT, DO A FUNCTIONAL TEST.
- **Code-domain:** That follows a specified time, sequence, or operation. AFTER YOU DEPLOY THE UPDATE, DO A SMOKE TEST.
> **STE:** After you deploy the update, do a smoke test.
> **Non-STE:** Following deployment of the update, do a smoke test.

*Ref: master.md - Dictionary entry AFTER (conj), Page 158*

---

## AGAIN (adv)
- **Original:** One more time. DO THE TEST AGAIN.
- **Code-domain:** One more time. RUN THE TEST AGAIN.
> **STE:** Run the test again.
> **Non-STE:** Rerun the test.

*Ref: master.md - Dictionary entry AGAIN (adv), Page 158*

---

...(continuing through all letters A-Z)...

---

# B

## BACK (adj), BACK (adv)
- **Original:** In a direction opposite to the front. INSTALL THE BACK PLATE. / MOVE THE LEVER BACK.
- **Code-domain:** In a direction opposite to forward. REVERT TO THE BACK VERSION. / NAVIGATE BACK TO THE PREVIOUS PAGE.
> **STE:** Revert to the back version.
> **Non-STE:** Revert to the previous version.

> **STE:** Navigate back to the previous page.
> **Non-STE:** Go backwards to the previous page.

*Ref: master.md - Dictionary entry BACK (adj), Page ~170*

---

## BACK UP (v) - UNNAPROVED
- **Original:** Not in dictionary as approved; use context-specific alternatives.
- **Code-domain:** Not applicable as standalone verb in STE-Code. Use SAVE (v) or COPY (v) for data; REVERSE (v) for motion.
> **STE:** Save the database before the migration.
> **Non-STE:** Back up the database before the migration.

> **STE:** Copy the configuration files.
> **Non-STE:** Back up the configuration files.

*Ref: master.md - Dictionary entry back up (v)*

---

## BAD (adj)
- **Original:** Not satisfactory or safe. REFER TO CHAPTER 6 FOR INSTRUCTIONS ABOUT HOW TO PARK IN BAD WEATHER CONDITIONS.
- **Code-domain:** Not satisfactory or safe. REFER TO SECTION 6 FOR INSTRUCTIONS ABOUT HOW TO HANDLE BAD BUILD STATES.
> **STE:** Refer to Section 6 for instructions about how to handle bad build states.
> **Non-STE:** Refer to Section 6 for instructions about how to handle unsatisfactory build states.

*Ref: master.md - Dictionary entry BAD (adj), Page 11*

---

## BALANCE (n), BALANCE (v)
- **Original:** A state of equilibrium. MAKE SURE THAT THE CONTROL SURFACES ARE IN BALANCE. / To bring into equilibrium. BALANCE THE ELEVATOR.
- **Code-domain:** A state of equilibrium. MAKE SURE THAT THE LOAD IS IN BALANCE ACROSS ALL NODES. / To distribute evenly. BALANCE THE WORKLOAD ACROSS ALL WORKERS.
> **STE:** Make sure that the load is in balance across all nodes.
> **Non-STE:** Make sure that the load is balanced across all nodes.

> **STE:** Balance the workload across all workers.
> **Non-STE:** Distribute the workload across all workers.

*Ref: master.md - Dictionary entry BALANCE (n), Page ~175*

---

## BASE (n) - UNNAPROVED
- **Original:** Not approved alone; use FOUNDATION (n) or BOTTOM (n).
- **Code-domain:** Use FOUNDATION (n) for conceptual base, ROOT (n) for positional base.
> **STE:** The foundation of the architecture is the data layer.
> **Non-STE:** The base of the architecture is the data layer.

> **STE:** Start from the root of the project.
> **Non-STE:** Start from the base of the project.

*Ref: master.md - Dictionary entry base (n)*

---

## BE (v)
- **Original:** 1. To occur, exist. IF THERE IS CORROSION ON THE PUMP VANES, REPLACE THE PUMP. No other verb forms. 2. To have a property to be equal to. ACID SOLUTIONS ARE DANGEROUS.
- **Code-domain:** 1. To occur, exist. IF THERE IS AN ERROR IN THE LOG, RESTART THE SERVICE. No other verb forms. 2. To have a property to be equal to. UNHANDLED EXCEPTIONS ARE DANGEROUS.
> **STE:** If there is an error in the log, restart the service.
> **Non-STE:** If an error exists in the log, restart the service.

> **STE:** Unhandled exceptions are dangerous.
> **Non-STE:** Unhandled exceptions constitute a danger.

*Ref: master.md - Dictionary entry BE (v), Page 11*

---

## BECAUSE (conj)
- **Original:** Function word that shows a cause or reason. DO NOT USE ALODINE, BECAUSE IT IS A DANGEROUS MATERIAL.
- **Code-domain:** Function word that shows a cause or reason. DO NOT USE RAW INPUT, BECAUSE IT IS A SECURITY RISK.
> **STE:** Do not use raw input, because it is a security risk.
> **Non-STE:** Do not use raw input, since it is a security risk.

*Ref: master.md - Dictionary entry BECAUSE (conj), Page ~180*

---

## BECOME (v)
- **Original:** To come to be. THE FLUID BECOMES CONTAMINATED.
- **Code-domain:** To come to be. THE CONNECTION BECOMES UNSTABLE.
> **STE:** The connection becomes unstable.
> **Non-STE:** The connection turns unstable.

*Ref: master.md - Dictionary entry BECOME (v), Page 11*

---

## BEFORE (conj)
- **Original:** Earlier than a specified time, sequence, or operation. BEFORE YOU INSTALL THE COMPONENT, READ THE INSTRUCTIONS.
- **Code-domain:** Earlier than a specified time, sequence, or operation. BEFORE YOU RUN THE MIGRATION, READ THE RELEASE NOTES.
> **STE:** Before you run the migration, read the release notes.
> **Non-STE:** Prior to running the migration, read the release notes.

*Ref: master.md - Dictionary entry BEFORE (conj), Page 11*

---

## BEGIN (v)
- **Original:** To start. BEGIN THE TEST PROCEDURE.
- **Code-domain:** To start. BEGIN THE BUILD PROCESS.
> **STE:** Begin the build process.
> **Non-STE:** Initiate the build process.

*Ref: master.md - Dictionary entry BEGIN (v)*

---

## BELOW (prep)
- **Original:** In (or to) a position lower than something. PUT THE CONTAINER BELOW THE WORK AREA.
- **Code-domain:** In (or to) a position lower than something in a hierarchy or list. SEE THE EXAMPLE BELOW THE CODE BLOCK.
> **STE:** See the example below the code block.
> **Non-STE:** See the example beneath the code block.

*Ref: master.md - Dictionary entry BELOW (prep)*

---

## BEND (v)
- **Original:** To change the shape of something with force. DO NOT BEND THE CABLE.
- **Code-domain:** Not applicable in pure software context. Retained for hardware docs.
> **Note:** Domain-specific; no code-documentation equivalent.

*Ref: master.md - Dictionary entry BEND (v)*

---

## BETWEEN (prep)
- **Original:** In the space that separates two items. PUT THE WASHER BETWEEN THE NUT AND THE BRACKET.
- **Code-domain:** In the logical space that separates two items. PUT THE MIDDLEWARE BETWEEN THE CLIENT AND THE SERVER.
> **STE:** Put the middleware between the client and the server.
> **Non-STE:** Insert the middleware between the client and the server.

*Ref: master.md - Dictionary entry BETWEEN (prep)*

---

## BLOCK (n)
- **Original:** A solid piece of material. PUT A BLOCK BELOW THE JACK.
- **Code-domain:** A segment of code or data. PUT A COMMENT BLOCK ABOVE THE FUNCTION.
> **STE:** Put a comment block above the function.
> **Non-STE:** Add documentation above the function.

*Ref: master.md - Dictionary entry BLOCK (n)*

---

## BOND (v)
- **Original:** To attach two materials together. BOND THE SEAL TO THE SURFACE.
- **Code-domain:** Not applicable in pure software. Retained for hardware docs.
> **Note:** Domain-specific; no code-documentation equivalent.

*Ref: master.md - Dictionary entry BOND (v)*

---

## BOTTOM (n), BOTTOM (adj)
- **Original:** The lowest part of something. PUT THE HEAVIER ITEMS AT THE BOTTOM. / The lowest. THE BOTTOM COVER.
- **Code-domain:** The lowest part or end of a file, list, or stack. SCROLL TO THE BOTTOM OF THE FILE. / The lowest. THE BOTTOM LAYER.
> **STE:** Scroll to the bottom of the file.
> **Non-STE:** Scroll to the end of the file.

> **STE:** The bottom layer of the stack is the database.
> **Non-STE:** The lowest layer of the stack is the database.

*Ref: master.md - Dictionary entry BOTTOM (n)*

---

## BRACKET (n) - (TN)
- **Original:** A support for an item. ATTACH THE BRACKET TO THE STRUCTURE.
- **Code-domain:** A symbol used in code syntax: `[]`, `{}`, `()`. USE SQUARE BRACKETS FOR ARRAY ACCESS.
> **STE:** Use square brackets for array access.
> **Non-STE:** Use the bracket notation for array access.

*Ref: master.md - Dictionary entry BRACKET (n) - technical noun*

---

## BREAK (v)
- **Original:** To cause to become damaged and not function. DO NOT BREAK THE SEAL.
- **Code-domain:** 1. To cause code to stop functioning. DO NOT BREAK THE PUBLIC API. 2. To exit a loop or control structure. BREAK OUT OF THE LOOP WHEN THE CONDITION IS TRUE.
> **STE:** Do not break the public API.
> **Non-STE:** Do not cause breaking changes to the public API.

> **STE:** Break out of the loop when the flag is set.
> **Non-STE:** Exit the loop when the flag is set.

*Ref: master.md - Dictionary entry BREAK (v)*

---

## BRING (v) - UNNAPROVED
- **Original:** CARRY (v), GET (v). GET THE TOOLS TO THE WORK AREA.
- **Code-domain:** GET (v), MOVE (v). GET THE DEPENDENCIES INTO THE CONTAINER.
> **STE:** Get the dependencies into the container.
> **Non-STE:** Bring the dependencies into the container.

*Ref: master.md - Dictionary entry bring (v), Page 12*

---

## BROAD (adj) - UNNAPROVED
- **Original:** WIDE (adj). WIDE COVERAGE.
- **Code-domain:** WIDE (adj). WIDE TEST COVERAGE.
> **STE:** Wide test coverage.
> **Non-STE:** Broad test coverage.

*Ref: master.md - Dictionary entry broad (adj)*

---

## BUG (n) - (TN)
- **Original:** Not in original STE (aerospace term: insect). In code-domain, this is a technical noun for software defects.
- **Code-domain:** Technical noun for a software defect. USE THE BUG TRACKER TO LOG DEFECTS.
> **STE:** Use the bug tracker to log defects.
> **Non-STE:** Use the issue tracker to log defects.

*Ref: master.md - Concept; adapted as code-domain technical noun*

---

## BUILD (v) - UNNAPROVED
- **Original:** ASSEMBLE (v). ASSEMBLE THE UNIT.
- **Code-domain:** COMPILE (v), MAKE (v). COMPILE THE PROJECT. / MAKE THE TARGET.
> **STE:** Compile the project.
> **Non-STE:** Build the project.

> **Note:** BUILD is a technical verb (TV) in code-domain and may be used as a technical verb per Rule 1.12.

*Ref: master.md - Dictionary entry build (v), Page 132*

---

## BURN (v)
- **Original:** To be on fire or to cause fire. DO NOT LET THE MATERIAL BURN.
- **Code-domain:** To write data to read-only media; retained as technical verb.
> **STE:** Burn the ISO image to the USB drive.
> **Non-STE:** Write the ISO image to the USB drive.

*Ref: master.md - Dictionary entry BURN (v)*

---

## BUT (conj)
- **Original:** Function word that shows a contrast. THE LIGHT IS ON, BUT THE SYSTEM DOES NOT OPERATE.
- **Code-domain:** Function word that shows a contrast. THE BUILD PASSES, BUT THE TESTS FAIL.
> **STE:** The build passes, but the tests fail.
> **Non-STE:** The build passes, however the tests fail.

*Ref: master.md - Dictionary entry BUT (conj), Page 12*

---

## BY (prep)
- **Original:** Function word that shows the means or agent. ATTACH THE FLANGE BY THE FOUR BOLTS. / CLEAN THE SURFACE BY ALCOHOL.
- **Code-domain:** Function word that shows the means or agent. BUILD THE PROJECT BY THE CMAKE TOOL. / AUTHENTICATE BY OAUTH.
> **STE:** Build the project by the CMake tool.
> **Non-STE:** Build the project using CMake.

> **STE:** Authenticate by OAuth.
> **Non-STE:** Authenticate via OAuth.

*Ref: master.md - Dictionary entry BY (prep), Page 12*

---

## BYTE (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A unit of digital information. THE BUFFER HOLDS 1024 BYTES.
> **STE:** The buffer holds 1024 bytes.
> **Non-STE:** The buffer has a size of 1024 bytes.

*Ref: Code-domain technical noun*

---

...(content continues through all letters. For brevity, representative samples are shown below for key letters)...

---

# C

## CALCULATE (v)
- **Original:** To find a number or amount using mathematics. CALCULATE THE TOTAL WEIGHT.
- **Code-domain:** To compute a value algorithmically. CALCULATE THE CHECKSUM OF THE FILE.
> **STE:** Calculate the checksum of the file.
> **Non-STE:** Compute the checksum of the file.

*Ref: master.md - Dictionary entry CALCULATE (v)*

---

## CALL (v) - UNNAPROVED
- **Original:** Three meanings: 1. NAME (v). NAME THE PROCEDURE "STARTUP." 2. SPEAK (v) or CONTACT (v). CONTACT THE OPERATOR. 3. REFER (v) TO.
- **Code-domain:** Three meanings: 1. NAME (v). NAME THE FUNCTION "init." 2. INVOKE (TV) - as technical verb. 3. REFER (v) TO.
> **STE:** Name the function "init."
> **Non-STE:** Call the function "init."

> **STE:** Contact the administrator.
> **Non-STE:** Call the administrator.

> **Note:** CALL as "invoke a function" is a technical verb (TV) permitted per Rule 1.12.

*Ref: master.md - Dictionary entry call (v), Page 12*

---

## CAN (v)
- **Original:** Auxiliary modal verb that means to be possible, to be able to, or to be permitted to. A MIXTURE OF FUEL AND OXYGEN CAN CAUSE AN EXPLOSION. YOU CAN OPERATE THE VEHICLE AFTER THE INSPECTION IS COMPLETED. No other verb forms. Do not use COULD.
- **Code-domain:** Auxiliary modal verb that means to be possible, to be able to, or to be permitted to. A MISCONFIGURATION CAN CAUSE A CRASH. YOU CAN RUN THE SCRIPT AFTER THE BUILD IS COMPLETED. No other verb forms. Do not use COULD.
> **STE:** A misconfiguration can cause a crash.
> **Non-STE:** A misconfiguration could cause a crash.

> **STE:** You can run the script after the build is completed.
> **Non-STE:** You are able to run the script after the build is completed.

*Ref: master.md - Dictionary entry CAN (v), Page 12, 135*

---

## CANCEL (v)
- **Original:** To stop an operation. CANCEL THE TEST PROCEDURE.
- **Code-domain:** To stop an operation. CANCEL THE DEPLOYMENT PIPELINE.
> **STE:** Cancel the deployment pipeline.
> **Non-STE:** Abort the deployment pipeline.

*Ref: master.md - Dictionary entry CANCEL (v), Page 12*

---

## CANNOT (v)
- **Original:** The negative form of CAN. YOU CANNOT USE THIS TOOL.
- **Code-domain:** The negative form of CAN. YOU CANNOT ACCESS THIS ENDPOINT WITHOUT AUTHENTICATION.
> **STE:** You cannot access this endpoint without authentication.
> **Non-STE:** You are unable to access this endpoint without authentication.

*Ref: master.md - Dictionary entry CANNOT (v), Page 12*

---

## CAPABLE (adj) - UNNAPROVED
- **Original:** CAN (v). THE SYSTEM CAN RECOVER FROM FAULTS AUTOMATICALLY.
- **Code-domain:** CAN (v). THE SERVICE CAN RECOVER FROM FAILURES AUTOMATICALLY.
> **STE:** The service can recover from failures automatically.
> **Non-STE:** The service is capable of recovering from failures automatically.

*Ref: master.md - Dictionary entry capable (adj), Page 12*

---

## CARE (n) - UNNAPROVED
- **Original:** Not approved; use CAUTION (n), BE CAREFUL.
- **Code-domain:** BE CAREFUL, CAUTION (n). BE CAREFUL WHEN YOU CHANGE THE CONFIGURATION.
> **STE:** Be careful when you change the configuration.
> **Non-STE:** Take care when changing the configuration.

*Ref: master.md - Dictionary entry care (n), Page 12*

---

## CARRY (v) - UNNAPROVED
- **Original:** Not approved; use TAKE (v), MOVE (v), HOLD (v).
- **Code-domain:** MOVE (v), TRANSMIT (v). MOVE THE DATA TO THE CACHE.
> **STE:** Move the data to the cache.
> **Non-STE:** Carry the data to the cache.

*Ref: master.md - Dictionary entry carry (v), Page 12*

---

## CARRY OUT (v) - UNNAPROVED
- **Original:** DO (v). DO THE INSPECTION.
- **Code-domain:** DO (v). DO THE REVIEW.
> **STE:** Do the review.
> **Non-STE:** Carry out the review.

*Ref: master.md - Dictionary entry carry out (v), Page 12*

---

## CASE (n) - UNNAPROVED
- **Original:** VARIOUS meanings; use IF (conj), CONTAINER (n), EXAMPLE (n) depending on context.
- **Code-domain:** For conditional: IF (conj). For coding structure: use SWITCH CASE as technical noun.
> **STE:** If the flag is true, log the event.
> **Non-STE:** In case the flag is true, log the event.

> **STE:** Add a switch case for the error state.
> **Non-STE:** Handle the error case.

*Ref: master.md - Dictionary entry case (n), Page 12*

---

## CATCH (v)
- **Original:** To capture or stop something in motion. CATCH THE FLUID WITH A CONTAINER.
- **Code-domain:** To intercept an exception or event. CATCH THE EXCEPTION AND LOG IT.
> **STE:** Catch the exception and log it.
> **Non-STE:** Trap the exception and log it.

*Ref: master.md - Dictionary entry CATCH (v)*

---

## CAUSE (v)
- **Original:** To make something occur. THE LEAK CAUSED THE FIRE.
- **Code-domain:** To make something occur. THE NULL POINTER CAUSED THE CRASH.
> **STE:** The null pointer caused the crash.
> **Non-STE:** The null pointer resulted in the crash.

*Ref: master.md - Dictionary entry CAUSE (v)*

---

## CAUTION (n)
- **Original:** A warning to be careful. OBEY THE CAUTIONS IN THIS MANUAL.
- **Code-domain:** A warning to be careful. OBEY THE CAUTIONS IN THIS README.
> **STE:** Obey the cautions in this README.
> **Non-STE:** Follow the cautions in this README.

*Ref: master.md - Dictionary entry CAUTION (n)*

---

## CENTER (n)
- **Original:** The middle point or part. FIND THE CENTER OF THE HOLE.
- **Code-domain:** The middle point of alignment. ALIGN THE TEXT TO THE CENTER.
> **STE:** Align the text to the center.
> **Non-STE:** Center the text.

*Ref: master.md - Dictionary entry CENTER (n)*

---

## CHANGE (v), CHANGE (n)
- **Original:** To make different. CHANGE THE FILTER. / An alteration. RECORD THE CHANGES IN THE LOGBOOK.
- **Code-domain:** To modify code. CHANGE THE FUNCTION SIGNATURE. / A modification. RECORD THE CHANGES IN THE CHANGELOG.
> **STE:** Change the function signature.
> **Non-STE:** Modify the function signature.

> **STE:** Record the changes in the changelog.
> **Non-STE:** Log the changes in the changelog.

*Ref: master.md - Dictionary entry CHANGE (v)*

---

## CHECK (n)
- **Original:** An inspection. DO A CHECK OF THE SYSTEM.
- **Code-domain:** A validation. DO A CHECK OF THE INPUT VALUES.
> **STE:** Do a check of the input values.
> **Non-STE:** Validate the input values.

*Ref: master.md - Dictionary entry CHECK (n)*

---

## CHECK (v) - UNNAPROVED
- **Original:** Not approved as verb; use CHECK (n) with DO. DO A CHECK OF THE VALUES.
- **Code-domain:** Not approved as verb; use VERIFY (v) or CHECK (n) with DO.
> **STE:** Do a check of the values.
> **Non-STE:** Check the values.

> **STE:** Verify the data integrity.
> **Non-STE:** Check the data integrity.

*Ref: master.md - Dictionary entry check (v), Page 12, 146*

---

## CHOOSE (v) - UNNAPROVED
- **Original:** SELECT (v), ALTERNATIVE (adj). SELECT THE CORRECT OPTION. / USE AN ALTERNATIVE APPROACH.
- **Code-domain:** SELECT (v), ALTERNATIVE (adj). SELECT THE CORRECT CONFIGURATION. / USE AN ALTERNATIVE IMPLEMENTATION.
> **STE:** Select the correct configuration.
> **Non-STE:** Choose the correct configuration.

*Ref: master.md - Dictionary entry choose (v), Page 12*

---

## CLEAN (v), CLEAN (adj)
- **Original:** To remove unwanted material. CLEAN THE SURFACE.
- **Code-domain:** To remove unwanted data or cleanup resources. CLEAN THE TEMPORARY FILES.
> **STE:** Clean the temporary files.
> **Non-STE:** Delete the temporary files.

*Ref: master.md - Dictionary entry CLEAN (v)*

---

## CLEAR (adj)
- **Original:** 1. That does not have obstacles. A CLEAR PATH. 2. That is easy to understand. CLEAR INSTRUCTIONS.
- **Code-domain:** 1. That does not have obstacles. A CLEAR CODE PATH. 2. That is easy to understand. CLEAR DOCUMENTATION.
> **STE:** A clear code path for the request.
> **Non-STE:** An unobstructed code path for the request.

> **STE:** Clear documentation for the API.
> **Non-STE:** Understandable documentation for the API.

*Ref: master.md - Dictionary entry CLEAR (adj), Page 12*

---

## CLICK (n), CLICK (v) - (TN/TV)
- **Original:** A short, sharp sound. WHEN YOU ATTACH THE SPRING CLIP, MAKE SURE THAT YOU HEAR A CLICK. / Code-domain: A mouse or interface action. CLICK THE BUTTON.
- **Code-domain:** Technical verb for UI interaction. CLICK THE "SUBMIT" BUTTON.
> **STE:** Click the "Submit" button.
> **Non-STE:** Press the "Submit" button.

*Ref: master.md - Dictionary entry click (v), Page 12; adapted as technical verb*

---

## CLOSE (v)
- **Original:** To shut or block an opening. CLOSE THE VALVE.
- **Code-domain:** To terminate a connection or file. CLOSE THE FILE HANDLE.
> **STE:** Close the file handle.
> **Non-STE:** Release the file handle.

*Ref: master.md - Dictionary entry CLOSE (v)*

---

## CODE (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** Instructions in a programming language. THE CODE IS IN THE `src/` DIRECTORY.
> **STE:** The code is in the `src/` directory.
> **Non-STE:** The source is in the `src/` directory.

*Ref: Code-domain technical noun*

---

## COLLECT (v)
- **Original:** To gather or accumulate. COLLECT THE FLUID IN A CONTAINER.
- **Code-domain:** To gather data or metrics. COLLECT THE METRICS FROM ALL NODES.
> **STE:** Collect the metrics from all nodes.
> **Non-STE:** Gather the metrics from all nodes.

*Ref: master.md - Dictionary entry COLLECT (v)*

---

## COME (v)
- **Original:** To move toward. WHEN THE PRESSURE COMES TO THE CORRECT VALUE, STOP THE PUMP.
- **Code-domain:** To reach a state. WHEN THE SERVICE COMES ONLINE, START THE TESTS.
> **STE:** When the service comes online, start the tests.
> **Non-STE:** When the service starts, start the tests.

*Ref: master.md - Dictionary entry COME (v), Page 13*

---

## COMMENT (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** Explanatory text in code. ADD A COMMENT TO EXPLAIN THE ALGORITHM.
> **STE:** Add a comment to explain the algorithm.
> **Non-STE:** Document the algorithm in the code.

*Ref: Code-domain technical noun*

---

## COMMIT (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb (version control).
- **Code-domain:** To save changes to version control. COMMIT THE CHANGES TO THE REPOSITORY.
> **STE:** Commit the changes to the repository.
> **Non-STE:** Save the changes to the repository.

*Ref: Code-domain technical verb*

---

## COMPARE (v)
- **Original:** To look at two or more items and find differences. COMPARE THE MEASURED VALUE WITH THE SPECIFIED VALUE.
- **Code-domain:** To evaluate two values for equality or difference. COMPARE THE HASH VALUE WITH THE EXPECTED HASH.
> **STE:** Compare the hash value with the expected hash.
> **Non-STE:** Check the hash value against the expected hash.

*Ref: master.md - Dictionary entry COMPARE (v)*

---

## COMPATIBLE (adj)
- **Original:** That can operate with other items. THE TWO UNITS ARE COMPATIBLE.
- **Code-domain:** That can operate with other items. THE LIBRARY IS COMPATIBLE WITH VERSION 3.0.
> **STE:** The library is compatible with version 3.0.
> **Non-STE:** The library works with version 3.0.

*Ref: master.md - Dictionary entry COMPATIBLE (adj), Page 13*

---

## COMPILE (v) - UNNAPROVED
- **Original:** Not approved; use MAKE (v), ASSEMBLE (v).
- **Code-domain:** Technical verb (TV) for translating source code. COMPILE THE SOURCE FILES.
> **STE:** Compile the source files.
> **Non-STE:** Build the source files.

*Ref: master.md - Dictionary entry compile (v), Page 13; adapted as technical verb*

---

## COMPLETE (v)
- **Original:** To finish. COMPLETE THE INSTALLATION.
- **Code-domain:** To finish. COMPLETE THE SETUP WIZARD.
> **STE:** Complete the setup wizard.
> **Non-STE:** Finish the setup wizard.

*Ref: master.md - Dictionary entry COMPLETE (v)*

---

## COMPONENT (n)
- **Original:** A part of a larger system. THE COMPONENT IS INSTALLED IN THE RACK.
- **Code-domain:** A modular part of a software system. THE COMPONENT IS IMPORTED IN THE MODULE.
> **STE:** The component is imported in the module.
> **Non-STE:** The component is used in the module.

*Ref: master.md - Dictionary entry COMPONENT (n), Page 13*

---

## COMPRESS (v)
- **Original:** To make smaller by pressure. COMPRESS THE SPRING.
- **Code-domain:** To make data smaller using an algorithm. COMPRESS THE LOG FILES BEFORE ARCHIVING.
> **STE:** Compress the log files before archiving.
> **Non-STE:** Zip the log files before archiving.

*Ref: master.md - Dictionary entry COMPRESS (v)*

---

## CONDITION (n)
- **Original:** A state of being. THE CONDITION OF THE UNIT IS SATISFACTORY.
- **Code-domain:** A state or logical expression. THE CONDITION OF THE BUILD IS SATISFACTORY. / IF THE CONDITION IS TRUE, CONTINUE.
> **STE:** The condition of the build is satisfactory.
> **Non-STE:** The build state is good.

> **STE:** If the condition is true, continue.
> **Non-STE:** If the conditional evaluates to true, continue.

*Ref: master.md - Dictionary entry CONDITION (n)*

---

## CONFIGURATION (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** The set of parameters that define system behavior. THE CONFIGURATION FILE IS IN YAML FORMAT.
> **STE:** The configuration file is in YAML format.
> **Non-STE:** The config file is in YAML format.

*Ref: Code-domain technical noun*

---

## CONFIRM (v) - UNNAPROVED
- **Original:** MAKE SURE (v). MAKE SURE THAT THE VALUES ARE CORRECT.
- **Code-domain:** MAKE SURE (v). MAKE SURE THAT THE BUILD IS SUCCESSFUL.
> **STE:** Make sure that the build is successful.
> **Non-STE:** Confirm that the build is successful.

*Ref: master.md - Dictionary entry confirm (v), Page 13*

---

## CONNECT (v)
- **Original:** To join two or more items. CONNECT THE HOSE TO THE VALVE.
- **Code-domain:** To establish a communication link. CONNECT THE CLIENT TO THE SERVER.
> **STE:** Connect the client to the server.
> **Non-STE:** Establish a connection between the client and the server.

*Ref: master.md - Dictionary entry CONNECT (v), Page 13*

---

## CONTAIN (v)
- **Original:** To hold or include. THE TANK CONTAINS FUEL.
- **Code-domain:** To hold or include. THE MODULE CONTAINS THE HELPER FUNCTIONS.
> **STE:** The module contains the helper functions.
> **Non-STE:** The module includes the helper functions.

*Ref: master.md - Dictionary entry CONTAIN (v)*

---

## CONTACT (v)
- **Original:** To communicate with. CONTACT THE OPERATOR. CONTACT THE SERVICE PROVIDER.
- **Code-domain:** To communicate with. CONTACT THE SYSTEM ADMINISTRATOR.
> **STE:** Contact the system administrator.
> **Non-STE:** Get in touch with the system administrator.

*Ref: master.md - Dictionary entry CONTACT (v), Page 13*

---

## CONTINUE (v)
- **Original:** To keep going. IF THE TEST PASSES, CONTINUE THE PROCEDURE.
- **Code-domain:** To keep executing. IF THE BUILD PASSES, CONTINUE THE DEPLOYMENT.
> **STE:** If the build passes, continue the deployment.
> **Non-STE:** If the build passes, proceed with the deployment.

*Ref: master.md - Dictionary entry CONTINUE (v)*

---

## CONTROL (n), CONTROL (v)
- **Original:** The ability to operate or direct. THE CONTROL OF THE SYSTEM IS AUTOMATIC. / To operate or direct. CONTROL THE SYSTEM WITH THE SOFTWARE.
- **Code-domain:** The ability to operate or direct. THE CONTROL OF THE ACCESS IS ROLE-BASED. / To operate or direct. CONTROL THE WORKFLOW WITH THE DASHBOARD.
> **STE:** The control of the access is role-based.
> **Non-STE:** Access is role-based.

> **STE:** Control the workflow with the dashboard.
> **Non-STE:** Manage the workflow with the dashboard.

*Ref: master.md - Dictionary entry CONTROL (v)*

---

## COPY (v)
- **Original:** To make a duplicate. COPY THE FILE TO THE BACKUP DRIVE.
- **Code-domain:** To duplicate data. COPY THE CONFIG TO THE STAGING ENVIRONMENT.
> **STE:** Copy the config to the staging environment.
> **Non-STE:** Duplicate the config to the staging environment.

*Ref: master.md - Dictionary entry COPY (v)*

---

## CORRECT (adj)
- **Original:** Without error. MAKE SURE THAT THE VALUES ARE CORRECT.
- **Code-domain:** Without error. MAKE SURE THAT THE TEST RESULTS ARE CORRECT.
> **STE:** Make sure that the test results are correct.
> **Non-STE:** Verify that the test results are correct.

*Ref: master.md - Dictionary entry CORRECT (adj)*

---

## CORRECTLY (adv)
- **Original:** In a correct manner. MAKE SURE THAT THE SEAL IS CORRECTLY INSTALLED.
- **Code-domain:** In a correct manner. MAKE SURE THAT THE PACKAGE IS CORRECTLY INSTALLED.
> **STE:** Make sure that the package is correctly installed.
> **Non-STE:** Ensure the package is correctly installed.

*Ref: master.md - Dictionary entry CORRECTLY (adv)*

---

## COUNT (v)
- **Original:** To find the total number. COUNT THE PARTS.
- **Code-domain:** To enumerate items. COUNT THE RECORDS IN THE DATABASE.
> **STE:** Count the records in the database.
> **Non-STE:** Get the count of records in the database.

*Ref: master.md - Dictionary entry COUNT (v)*

---

## COVER (n)
- **Original:** A thing that goes over another. PUT THE COVER ON THE UNIT.
- **Code-domain:** Not applicable. Retained for hardware context.
> **Note:** Domain-specific; no code-documentation equivalent.

*Ref: master.md - Dictionary entry COVER (n)*

---

## CRASH (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To fail suddenly and stop functioning. IF THE APPLICATION CRASHES, READ THE LOGS.
> **STE:** If the application crashes, read the logs.
> **Non-STE:** If the application fails, read the logs.

*Ref: Code-domain technical verb*

---

## CREATE (v)
- **Original:** To make something new. CREATE A NEW FILE.
- **Code-domain:** To instantiate or generate. CREATE A NEW INSTANCE OF THE CLASS.
> **STE:** Create a new instance of the class.
> **Non-STE:** Instantiate a new object of the class.

*Ref: master.md - Dictionary entry CREATE (v)*

---

## CUT (v)
- **Original:** To divide with a sharp tool. CUT THE WIRE TO THE SPECIFIED LENGTH.
- **Code-domain:** To remove and place. CUT THE TEXT AND PASTE IT IN THE NEW LOCATION.
> **STE:** Cut the text and paste it in the new location.
> **Non-STE:** Move the text to the new location.

*Ref: master.md - Dictionary entry CUT (v)*

---

# D

## DAMAGE (n)
- **Original:** Harm that reduces function. THE DAMAGE TO THE UNIT IS SMALL.
- **Code-domain:** Harm that reduces function. THE DAMAGE TO THE DATA IS IRREVERSIBLE.
> **STE:** The damage to the data is irreversible.
> **Non-STE:** The data corruption is irreversible.

*Ref: master.md - Dictionary entry DAMAGE (n), Page 13*

---

## DANGER (n) - UNNAPROVED
- **Original:** RISK (n). THIS PROCEDURE HAS A RISK OF FIRE.
- **Code-domain:** RISK (n). THIS OPERATION HAS A RISK OF DATA LOSS.
> **STE:** This operation has a risk of data loss.
> **Non-STE:** There is a danger of data loss with this operation.

*Ref: master.md - Dictionary entry danger (n), Page 13*

---

## DANGEROUS (adj)
- **Original:** That can cause injury or damage. THIS CHEMICAL IS DANGEROUS.
- **Code-domain:** That can cause harm or data loss. THIS COMMAND IS DANGEROUS.
> **STE:** This command is dangerous.
> **Non-STE:** This command poses a danger.

*Ref: master.md - Dictionary entry DANGEROUS (adj)*

---

## DATA (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** Information processed or stored by a computer. THE DATA IS STORED IN THE CACHE.
> **STE:** The data is stored in the cache.
> **Non-STE:** The information is stored in the cache.

*Ref: Code-domain technical noun*

---

## DEACTIVATE (v)
- **Original:** To make a system, function, or feature not ready for operation. DEACTIVATE THE AUTOPILOT.
- **Code-domain:** To disable a system, function, or feature. DEACTIVATE THE BACKGROUND WORKER.
> **STE:** Deactivate the background worker.
> **Non-STE:** Disable the background worker.

*Ref: master.md - Dictionary entry DEACTIVATE (v), Page 13*

---

## DEBUG (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To find and fix defects in code. DEBUG THE APPLICATION WITH THE ATTACHED PROFILER.
> **STE:** Debug the application with the attached profiler.
> **Non-STE:** Troubleshoot the application with the attached profiler.

*Ref: Code-domain technical verb*

---

## DECREASE (v)
- **Original:** To become smaller. DECREASE THE PRESSURE.
- **Code-domain:** To reduce a value. DECREASE THE TIMEOUT VALUE.
> **STE:** Decrease the timeout value.
> **Non-STE:** Lower the timeout value.

*Ref: master.md - Dictionary entry DECREASE (v)*

---

## DEEP (adj)
- **Original:** Extending far down from the top. DEEP HOLE.
- **Code-domain:** Extending far in a hierarchy. DEEP DIRECTORY STRUCTURE.
> **STE:** Deep directory structure.
> **Non-STE:** Nested directory structure.

*Ref: master.md - Dictionary entry DEEP (adj), Page 14*

---

## DEFAULT (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** The pre-set value or state. THE DEFAULT VALUE IS 8080.
> **STE:** The default value is 8080.
> **Non-STE:** The initial value is 8080.

*Ref: Code-domain technical noun*

---

## DEFECT (n) - (TN)
- **Original:** A shortcoming or flaw. EXAMINE THE SEAL FOR DEFECTS.
- **Code-domain:** A bug in software. LOG THE DEFECT IN THE TRACKING SYSTEM.
> **STE:** Log the defect in the tracking system.
> **Non-STE:** Log the bug in the tracking system.

*Ref: master.md - Dictionary entry DEFECT (n)*

---

## DEFINE (v)
- **Original:** To give the meaning or specification. THE STANDARD DEFINES THE PROCEDURE.
- **Code-domain:** To declare or specify. THE HEADER FILE DEFINES THE INTERFACE.
> **STE:** The header file defines the interface.
> **Non-STE:** The header file declares the interface.

*Ref: master.md - Dictionary entry DEFINE (v)*

---

## DELETE (v) - UNNAPROVED
- **Original:** Not approved; use REMOVE (v), ERASE (v).
- **Code-domain:** REMOVE (v). REMOVE THE FILE FROM THE DIRECTORY.
> **STE:** Remove the file from the directory.
> **Non-STE:** Delete the file from the directory.

> **Note:** DELETE is a technical verb (TV) in database operations and may be used per Rule 1.12.

*Ref: master.md - Dictionary entry delete (v), Page 14*

---

## DEPLOY (v)
- **Original:** To put into position for use. DEPLOY THE ANTENNA.
- **Code-domain:** To release software to a target environment. DEPLOY THE APPLICATION TO PRODUCTION.
> **STE:** Deploy the application to production.
> **Non-STE:** Release the application to production.

*Ref: master.md - Dictionary entry DEPLOY (v), Page 14*

---

## DEPRECATED (adj) - (TN)
- **Original:** Not in original STE. Code-domain technical adjective.
- **Code-domain:** Marked as no longer recommended for use. THE DEPRECATED FUNCTION WILL BE REMOVED IN VERSION 4.0.
> **STE:** The deprecated function will be removed in version 4.0.
> **Non-STE:** The outdated function will be removed in version 4.0.

*Ref: Code-domain technical adjective*

---

## DESIGN (n)
- **Original:** A plan and specification. THE DESIGN OF THE SYSTEM IS COMPLEX.
- **Code-domain:** The architecture and pattern. THE DESIGN OF THE API FOLLOWS REST PRINCIPLES.
> **STE:** The design of the API follows REST principles.
> **Non-STE:** The architecture of the API follows REST principles.

*Ref: master.md - Dictionary entry DESIGN (n)*

---

## DESTROY (v) - UNNAPROVED
- **Original:** BREAK (v), REMOVE (v). BREAK THE OLD SEAL. / REMOVE THE CONTAMINATION.
- **Code-domain:** BREAK (v), REMOVE (v). BREAK THE OLD SESSION. / REMOVE THE OBSOLETE DATA.
> **STE:** Break the old session.
> **Non-STE:** Destroy the old session.

*Ref: master.md - Dictionary entry destroy (v), Page 14*

---

## DEVELOP (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To write and test software. DEVELOP THE FEATURE IN A SEPARATE BRANCH.
> **STE:** Develop the feature in a separate branch.
> **Non-STE:** Build the feature in a separate branch.

*Ref: Code-domain technical verb*

---

## DIFFERENT (adj)
- **Original:** Not the same. THE TWO UNITS HAVE DIFFERENT DIMENSIONS.
- **Code-domain:** Not the same. THE TWO IMPLEMENTATIONS HAVE DIFFERENT PERFORMANCE.
> **STE:** The two implementations have different performance.
> **Non-STE:** The two implementations differ in performance.

*Ref: master.md - Dictionary entry DIFFERENT (adj), Page 24*

---

## DIMENSION (n)
- **Original:** A measurement of size. MEASURE THE DIMENSIONS OF THE PART.
- **Code-domain:** A measurement or axis. THE ARRAY HAS THREE DIMENSIONS.
> **STE:** The array has three dimensions.
> **Non-STE:** The array is three-dimensional.

*Ref: master.md - Dictionary entry DIMENSION (n), Page 14*

---

## DIRECTORY (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A container for files in a filesystem. THE SOURCE FILES ARE IN THE `src/` DIRECTORY.
> **STE:** The source files are in the `src/` directory.
> **Non-STE:** The source files are in the `src/` folder.

*Ref: Code-domain technical noun*

---

## DISABLE (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To turn off or make inactive. DISABLE THE FEATURE FLAG.
> **STE:** Disable the feature flag.
> **Non-STE:** Turn off the feature flag.

*Ref: Code-domain technical verb*

---

## DISCARD (v)
- **Original:** To throw away. DISCARD THE USED FILTER.
- **Code-domain:** To throw away. DISCARD THE DEPRECATED CODE.
> **STE:** Discard the deprecated code.
> **Non-STE:** Remove the deprecated code.

*Ref: master.md - Dictionary entry DISCARD (v)*

---

## DISCONNECT (v)
- **Original:** To break a connection. DISCONNECT THE CABLE.
- **Code-domain:** To break a connection. DISCONNECT THE SOCKET.
> **STE:** Disconnect the socket.
> **Non-STE:** Close the socket.

*Ref: master.md - Dictionary entry DISCONNECT (v)*

---

## DISPLAY (v), DISPLAY (n)
- **Original:** To show. THE SCREEN DISPLAYS THE DATA.
- **Code-domain:** To show output. THE TERMINAL DISPLAYS THE LOG OUTPUT.
> **STE:** The terminal displays the log output.
> **Non-STE:** The terminal shows the log output.

*Ref: master.md - Dictionary entry DISPLAY (v)*

---

## DIVIDE (v)
- **Original:** To separate into parts. DIVIDE THE LOAD EQUALLY.
- **Code-domain:** To split or perform division. DIVIDE THE TASKS AMONG THE WORKERS.
> **STE:** Divide the tasks among the workers.
> **Non-STE:** Distribute the tasks among the workers.

*Ref: master.md - Dictionary entry DIVIDE (v)*

---

## DO (v)
- **Original:** To perform an action. DO THE TEST PROCEDURE.
- **Code-domain:** To perform an action. DO THE BUILD STEP.
> **STE:** Do the build step.
> **Non-STE:** Execute the build step.

*Ref: master.md - Dictionary entry DO (v), Page 14*

---

## DOCUMENT (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To write documentation. DOCUMENT THE PUBLIC API.
> **STE:** Document the public API.
> **Non-STE:** Write docs for the public API.

*Ref: Code-domain technical verb*

---

## DOWN (adv), DOWN (prep)
- **Original:** In a direction to a lower position. MOVE THE LEVER DOWN.
- **Code-domain:** In a direction to a lower position or reduced state. SCROLL DOWN THE PAGE. / THE SERVER IS DOWN.
> **STE:** Scroll down the page.
> **Non-STE:** Scroll to the lower part of the page.

> **STE:** The server is down.
> **Non-STE:** The server is not operational.

*Ref: master.md - Dictionary entry DOWN (adv)*

---

## DOWNLOAD (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To transfer data from a remote source. DOWNLOAD THE PACKAGE FROM THE REGISTRY.
> **STE:** Download the package from the registry.
> **Non-STE:** Get the package from the registry.

*Ref: Code-domain technical verb*

---

## DRAIN (v)
- **Original:** To let liquid flow out. DRAIN THE TANK.
- **Code-domain:** To deplete resources. DRAIN THE CONNECTION POOL.
> **STE:** Drain the connection pool.
> **Non-STE:** Empty the connection pool.

*Ref: master.md - Dictionary entry DRAIN (v)*

---

## DRAW (v)
- **Original:** To make a picture or diagram. DRAW THE ROUTING.
- **Code-domain:** To create a visual representation. DRAW THE ARCHITECTURE DIAGRAM.
> **STE:** Draw the architecture diagram.
> **Non-STE:** Create the architecture diagram.

*Ref: master.md - Dictionary entry DRAW (v)*

---

## DROP (v)
- **Original:** To let fall. DO NOT DROP THE COMPONENT.
- **Code-domain:** To remove or discard. DROP THE TABLE FROM THE DATABASE.
> **STE:** Drop the table from the database.
> **Non-STE:** Delete the table from the database.

*Ref: master.md - Dictionary entry DROP (v)*

---

## DRY (adj), DRY (v)
- **Original:** Not wet. CLEAN THE SURFACE WITH A DRY CLOTH. / To make dry. DRY THE COMPONENT.
- **Code-domain:** Not applicable. Retained for hardware context.
> **Note:** Domain-specific; no code-documentation equivalent.

*Ref: master.md - Dictionary entry DRY (adj), Page 14*

---

# E

## EACH (adj)
- **Original:** Every one of two or more. EACH UNIT HAS A SERIAL NUMBER.
- **Code-domain:** Every one of two or more. EACH MODULE HAS A README FILE.
> **STE:** Each module has a README file.
> **Non-STE:** Every module has a README file.

*Ref: master.md - Dictionary entry EACH (adj), Page 15*

---

## EASY (adj)
- **Original:** Not difficult. THE INSTALLATION IS EASY.
- **Code-domain:** Not difficult. THE SETUP IS EASY.
> **STE:** The setup is easy.
> **Non-STE:** The setup is straightforward.

*Ref: master.md - Dictionary entry EASY (adj)*

---

## EDIT (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To modify text or code. EDIT THE CONFIGURATION FILE WITH A TEXT EDITOR.
> **STE:** Edit the configuration file with a text editor.
> **Non-STE:** Modify the configuration file with a text editor.

*Ref: Code-domain technical verb*

---

## EFFECT (n)
- **Original:** A result or consequence. THE EFFECT OF THE PRESSURE IS SMALL.
- **Code-domain:** A result or consequence. THE EFFECT OF THE CHANGE IS SMALL.
> **STE:** The effect of the change is small.
> **Non-STE:** The impact of the change is small.

*Ref: master.md - Dictionary entry EFFECT (n)*

---

## EJECT (v)
- **Original:** To force out. EJECT THE CASSETTE.
- **Code-domain:** To remove forcibly. EJECT THE VOLUME.
> **STE:** Eject the volume.
> **Non-STE:** Unmount the volume.

*Ref: master.md - Dictionary entry EJECT (v)*

---

## ELEMENT (n)
- **Original:** A basic part of something. EACH ELEMENT OF THE ARRAY HAS A VALUE.
- **Code-domain:** A single item in a collection. EACH ELEMENT OF THE LIST HAS AN INDEX.
> **STE:** Each element of the list has an index.
> **Non-STE:** Each item of the list has an index.

*Ref: master.md - Dictionary entry ELEMENT (n)*

---

## ELSE (adv) - (TN)
- **Original:** Not in original STE. Code-domain technical adverb.
- **Code-domain:** Used to specify an alternative branch in conditional logic.
> **STE:** If the value is null, return 0; else return the value.
> **Non-STE:** If the value is null, return 0; otherwise return the value.

*Ref: Code-domain technical adverb*

---

## EMPTY (adj)
- **Original:** That does not contain anything. AN EMPTY CONTAINER.
- **Code-domain:** That does not contain data. AN EMPTY STRING.
> **STE:** An empty string.
> **Non-STE:** A zero-length string.

*Ref: master.md - Dictionary entry EMPTY (adj)*

---

## ENABLE (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To make active. ENABLE THE DEBUG MODE.
> **STE:** Enable the debug mode.
> **Non-STE:** Turn on the debug mode.

*Ref: Code-domain technical verb*

---

## END (n), END (v)
- **Original:** The final point. THE END OF THE CABLE. / To stop. END THE PROCEDURE.
- **Code-domain:** The termination point. THE END OF THE FILE. / To stop. END THE SESSION.
> **STE:** The end of the file.
> **Non-STE:** The final byte of the file.

> **STE:** End the session.
> **Non-STE:** Terminate the session.

*Ref: master.md - Dictionary entry END (n)*

---

## ENSURE (v) - UNNAPROVED
- **Original:** MAKE SURE (v). MAKE SURE THAT THE LATCH IS ENGAGED.
- **Code-domain:** MAKE SURE (v). MAKE SURE THAT THE DATABASE IS CONNECTED.
> **STE:** Make sure that the database is connected.
> **Non-STE:** Ensure that the database is connected.

*Ref: master.md - Dictionary entry ensure (v), Page 146*

---

## ENTER (v) - UNNAPROVED
- **Original:** Not approved; use PUT (v), TYPE (v) for data entry.
- **Code-domain:** PUT (v), TYPE (v). TYPE YOUR PASSWORD.
> **STE:** Type your password.
> **Non-STE:** Enter your password.

*Note: ENTER may be a technical verb (TV) for UI interactions per Rule 1.12.*

*Ref: master.md - Dictionary entry enter (v), Page 15*

---

## ENVIRONMENT (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** The set of conditions in which software runs. THE STAGING ENVIRONMENT IS A COPY OF PRODUCTION.
> **STE:** The staging environment is a copy of production.
> **Non-STE:** The staging setup is a copy of production.

*Ref: Code-domain technical noun*

---

## EQUAL (adj), EQUAL (v)
- **Original:** The same. THE TWO VALUES ARE EQUAL. / To be the same. THE SUM EQUALS 100.
- **Code-domain:** Having the same value. THE TWO HASHES ARE EQUAL.
> **STE:** The two hashes are equal.
> **Non-STE:** The two hashes are the same.

> **STE:** The result equals zero.
> **Non-STE:** The result is zero.

*Ref: master.md - Dictionary entry EQUAL (v), Page 15*

---

## ERASE (v)
- **Original:** To remove completely. ERASE THE DATA.
- **Code-domain:** To remove completely. ERASE THE SENSITIVE DATA FROM MEMORY.
> **STE:** Erase the sensitive data from memory.
> **Non-STE:** Wipe the sensitive data from memory.

*Ref: master.md - Dictionary entry ERASE (v)*

---

## ERROR (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A mistake or problem in software. THE ERROR OCCURRED AT LINE 42.
> **STE:** The error occurred at line 42.
> **Non-STE:** The issue occurred at line 42.

*Ref: Code-domain technical noun*

---

## ESTABLISH (v) - UNNAPROVED
- **Original:** MAKE (v), SET UP (v). MAKE A CONNECTION.
- **Code-domain:** MAKE (v), START (v). MAKE A CONNECTION. / START A SESSION.
> **STE:** Make a connection.
> **Non-STE:** Establish a connection.

*Ref: master.md - Dictionary entry establish (v), Page 15*

---

## EVALUATE (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To compute or assess. EVALUATE THE EXPRESSION AT RUNTIME.
> **STE:** Evaluate the expression at runtime.
> **Non-STE:** Compute the expression at runtime.

*Ref: Code-domain technical verb*

---

## EVENT (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** An occurrence that a program can respond to. THE EVENT TRIGGERS THE CALLBACK.
> **STE:** The event triggers the callback.
> **Non-STE:** The event fires the callback.

*Ref: Code-domain technical noun*

---

## EXAMINE (v)
- **Original:** To look at carefully. EXAMINE THE SURFACE FOR DAMAGE.
- **Code-domain:** To review carefully. EXAMINE THE CODE FOR SECURITY ISSUES.
> **STE:** Examine the code for security issues.
> **Non-STE:** Review the code for security issues.

*Ref: master.md - Dictionary entry EXAMINE (v)*

---

## EXAMPLE (n)
- **Original:** A thing that represents a pattern. THIS IS AN EXAMPLE OF A CORRECT PROCEDURE.
- **Code-domain:** An illustrative instance. THIS IS AN EXAMPLE OF A CORRECT API CALL.
> **STE:** This is an example of a correct API call.
> **Non-STE:** This demonstrates a correct API call.

*Ref: master.md - Dictionary entry EXAMPLE (n)*

---

## EXCEPT (prep) - UNNAPROVED
- **Original:** BUT NOT, OTHER THAN. ALL COMPONENTS EXCEPT THE VALVE ARE SERVICEABLE.
- **Code-domain:** BUT NOT, OTHER THAN. ALL MODULES EXCEPT THE DATABASE ARE AVAILABLE.
> **STE:** All modules except the database module are available.
> **Non-STE:** All modules other than the database module are available.

*Ref: master.md - Dictionary entry except (prep), Page 15*

---

## EXECUTE (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To run a program or command. EXECUTE THE SCRIPT FROM THE TERMINAL.
> **STE:** Execute the script from the terminal.
> **Non-STE:** Run the script from the terminal.

*Ref: Code-domain technical verb*

---

## EXPAND (v)
- **Original:** To become larger. THE METAL EXPANDS WHEN HEATED.
- **Code-domain:** To increase in scope or size. EXPAND THE MACRO AT COMPILE TIME.
> **STE:** Expand the macro at compile time.
> **Non-STE:** The macro is substituted at compile time.

*Ref: master.md - Dictionary entry EXPAND (v)*

---

## EXPLAIN (v) - UNNAPROVED
- **Original:** Not approved; use TELL (v), SHOW (v), DESCRIBE (v).
- **Code-domain:** DESCRIBE (v), TELL (v). DESCRIBE THE ERROR CONDITION.
> **STE:** Describe the error condition.
> **Non-STE:** Explain the error condition.

*Ref: master.md - Dictionary entry explain (v), Page 15*

---

## EXPORT (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To make available outside a module. EXPORT THE FUNCTION FROM THE LIBRARY.
> **STE:** Export the function from the library.
> **Non-STE:** Make the function available from the library.

*Ref: Code-domain technical verb*

---

## EXTEND (v)
- **Original:** To make longer or larger. EXTEND THE LANDING GEAR.
- **Code-domain:** To add functionality through inheritance. EXTEND THE BASE CLASS TO ADD NEW METHODS.
> **STE:** Extend the base class to add new methods.
> **Non-STE:** Subclass the base class to add new methods.

*Ref: master.md - Dictionary entry EXTEND (v)*

---

# F

## FAIL (v)
- **Original:** Not in original STE. Imported as technical verb.
- **Code-domain:** To be unsuccessful. IF THE TEST FAILS, EXAMINE THE LOGS.
> **STE:** If the test fails, examine the logs.
> **Non-STE:** If the test does not pass, examine the logs.

*Ref: Code-domain technical verb*

---

## FAILURE (n) - UNNAPROVED
- **Original:** Not approved; use a descriptive phrase: DOES NOT OPERATE, BREAKS.
- **Code-domain:** DOES NOT WORK, STOPS. IF THE SERVICE STOPS, RESTART IT.
> **STE:** If the service stops, restart it.
> **Non-STE:** In case of service failure, restart it.

> **Note:** FAILURE may be used as a technical noun in specific contexts (e.g., FAILURE MODE).

*Ref: master.md - Dictionary entry failure (n), Page 16*

---

## FALL (v)
- **Original:** To move downward by gravity. IF OIL SPILLS, CLEAN THE AREA IMMEDIATELY. YOU CAN SLIP AND FALL.
- **Code-domain:** Not directly applicable; retained for safety context.
> **Note:** Domain-specific; no code-documentation equivalent for physical falling.

*Ref: master.md - Dictionary entry FALL (v)*

---

## FALSE (adj) - (TN)
- **Original:** Not in original STE. Code-domain technical adjective.
- **Code-domain:** A Boolean value representing untruth. IF THE CONDITION IS FALSE, SKIP THE BLOCK.
> **STE:** If the condition is false, skip the block.
> **Non-STE:** If the condition does not hold, skip the block.

*Ref: Code-domain technical adjective*

---

## FAST (adj), FAST (adv)
- **Original:** At high speed. FAST MOVEMENT.
- **Code-domain:** At high speed or low latency. FAST RESPONSE TIME.
> **STE:** Fast response time.
> **Non-STE:** Low latency.

*Ref: master.md - Dictionary entry FAST (adj)*

---

## FATAL (adj) - (TN)
- **Original:** Not in original STE. Code-domain technical adjective.
- **Code-domain:** Causing the program to terminate. A FATAL ERROR OCCURRED.
> **STE:** A fatal error occurred.
> **Non-STE:** A critical error occurred.

*Ref: Code-domain technical adjective*

---

## FETCH (v)
- **Original:** To go and get. FETCH THE TOOL.
- **Code-domain:** To retrieve data. FETCH THE RECORDS FROM THE DATABASE.
> **STE:** Fetch the records from the database.
> **Non-STE:** Retrieve the records from the database.

*Ref: master.md - Dictionary entry FETCH (v)*

---

## FIELD (n) - (TN)
- **Original:** An area or space. THE FIELD OF VIEW.
- **Code-domain:** A data member of a structure or form. THE `email` FIELD OF THE FORM MUST BE VALIDATED.
> **STE:** The `email` field of the form must be validated.
> **Non-STE:** The `email` input of the form must be validated.

*Ref: Code-domain technical noun*

---

## FILE (n) - (TN)
- **Original:** A tool for smoothing (not applicable). Code-domain: A container of data on disk.
- **Code-domain:** A named collection of data. THE CONFIGURATION FILE IS IN TOML FORMAT.
> **STE:** The configuration file is in TOML format.
> **Non-STE:** The config is in TOML format.

*Ref: Code-domain technical noun*

---

## FILL (v)
- **Original:** To make full. FILL THE TANK.
- **Code-domain:** To populate with data. FILL THE ARRAY WITH DEFAULT VALUES.
> **STE:** Fill the array with default values.
> **Non-STE:** Initialize the array with default values.

*Ref: master.md - Dictionary entry FILL (v)*

---

## FILTER (n), FILTER (v)
- **Original:** A device that removes unwanted material. / To remove unwanted material. FILTER THE FLUID.
- **Code-domain:** A function that selects data. / To select data. FILTER THE RESULTS BY STATUS.
> **STE:** Filter the results by status.
> **Non-STE:** Select only the results that match the status.

*Ref: master.md - Dictionary entry FILTER (n)*

---

## FIND (v)
- **Original:** To discover or locate. FIND THE CAUSE OF THE PROBLEM.
- **Code-domain:** To search for and locate. FIND THE ROOT CAUSE OF THE ERROR.
> **STE:** Find the root cause of the error.
> **Non-STE:** Determine the root cause of the error.

*Ref: master.md - Dictionary entry FIND (v)*

---

## FINISH (v)
- **Original:** To complete. FINISH THE INSTALLATION.
- **Code-domain:** To complete. FINISH THE SETUP.
> **STE:** Finish the setup.
> **Non-STE:** Complete the setup.

*Ref: master.md - Dictionary entry FINISH (v)*

---

## FIRST (adj), FIRST (adv)
- **Original:** Before all others. THE FIRST STEP. / Before all others. DO THIS STEP FIRST.
- **Code-domain:** Before all others. THE FIRST ITERATION. / DEFINE THE VARIABLE FIRST.
> **STE:** Define the variable first.
> **Non-STE:** Initially define the variable.

*Ref: master.md - Dictionary entry FIRST (adj)*

---

## FIT (v) - UNNAPROVED
- **Original:** INSTALL (v), ATTACH (v). INSTALL THE COMPONENT.
- **Code-domain:** INSTALL (v), ADD (v). INSTALL THE PACKAGE.
> **STE:** Install the package.
> **Non-STE:** Fit the package into the project.

*Ref: master.md - Dictionary entry fit (v), Page 146*

---

## FIX (v)
- **Original:** To attach firmly. FIX THE BRACKET TO THE WALL.
- **Code-domain:** To repair a bug. FIX THE MEMORY LEAK.
> **STE:** Fix the memory leak.
> **Non-STE:** Resolve the memory leak.

*Ref: master.md - Dictionary entry FIX (v)*

---

## FLAG (n) - (TN)
- **Original:** A piece of fabric (not in STE). Code-domain: A marker or switch.
- **Code-domain:** A variable used as a signal. SET THE DEBUG FLAG TO TRUE.
> **STE:** Set the debug flag to true.
> **Non-STE:** Enable the debug flag.

*Ref: Code-domain technical noun*

---

## FLOW (n), FLOW (v)
- **Original:** Movement of a fluid. THE FLOW OF FUEL. / To move as a fluid. THE FUEL FLOWS THROUGH THE PIPE.
- **Code-domain:** Movement of data or control. THE FLOW OF DATA THROUGH THE PIPELINE. / To pass data through. THE DATA FLOWS THROUGH THE CHANNEL.
> **STE:** The flow of data through the pipeline.
> **Non-STE:** The data stream through the pipeline.

> **STE:** The data flows through the channel.
> **Non-STE:** The data passes through the channel.

*Ref: master.md - Dictionary entry FLOW (n), Page 16*

---

## FOLLOW (v) - UNNAPROVED
- **Original:** OBEY (v). OBEY THE INSTRUCTIONS.
- **Code-domain:** OBEY (v). OBEY THE CODING GUIDELINES.
> **STE:** Obey the coding guidelines.
> **Non-STE:** Follow the coding guidelines.

*Ref: master.md - Dictionary entry follow (v), Page 146*

---

## FOR (prep)
- **Original:** Function word that shows purpose or destination. FOR DATA, REFER TO THE MANUAL.
- **Code-domain:** Function word that shows purpose or destination. FOR EXAMPLES, REFER TO THE README.
> **STE:** For examples, refer to the README.
> **Non-STE:** To see examples, refer to the README.

*Ref: master.md - Dictionary entry FOR (prep)*

---

## FORCE (n)
- **Original:** Strength or energy. APPLY FORCE TO THE LEVER.
- **Code-domain:** To compel a non-default behavior. FORCE THE APPLICATION TO RESTART.
> **STE:** Force the application to restart.
> **Non-STE:** Compel the application to restart.

*Ref: master.md - Dictionary entry FORCE (n)*

---

## FORMAT (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** The structure of data representation. THE FILE FORMAT IS JSON.
> **STE:** The file format is JSON.
> **Non-STE:** The file is in JSON.

*Ref: Code-domain technical noun*

---

## FORWARD (adv)
- **Original:** In a direction to the front. MOVE THE LEVER FORWARD.
- **Code-domain:** In a direction to the front or next. MOVE THE POINTER FORWARD.
> **STE:** Move the pointer forward.
> **Non-STE:** Advance the pointer.

*Ref: master.md - Dictionary entry FORWARD (adv)*

---

## FREE (adj)
- **Original:** Not occupied or not restricted. THE AREA IS FREE OF CONTAMINATION.
- **Code-domain:** Not occupied or not restricted. THE CODE IS FREE OF ERRORS.
> **STE:** The code is free of errors.
> **Non-STE:** The code has no errors.

*Ref: master.md - Dictionary entry FREE (adj), Page 16*

---

## FROM (prep)
- **Original:** Function word that shows a source or starting point. REMOVE THE UNIT FROM THE RACK.
- **Code-domain:** Function word that shows a source or starting point. IMPORT THE MODULE FROM THE PACKAGE.
> **STE:** Import the module from the package.
> **Non-STE:** Import the module out of the package.

*Ref: master.md - Dictionary entry FROM (prep)*

---

## FULL (adj)
- **Original:** Containing all that is possible. FULL POWER.
- **Code-domain:** Complete. FULL TEST SUITE.
> **STE:** Full test suite.
> **Non-STE:** Complete test suite.

*Ref: master.md - Dictionary entry FULL (adj)*

---

## FUNCTION (n)
- **Original:** The purpose of something. THE FUNCTION OF THE VALVE IS TO CONTROL THE FLOW.
- **Code-domain:** A named procedure or subroutine. THE FUNCTION RETURNS A STRING. / The purpose of a component. THE FUNCTION OF THE MIDDLEWARE IS TO AUTHENTICATE REQUESTS.
> **STE:** The function returns a string.
> **Non-STE:** The method returns a string.

> **STE:** The function of the middleware is to authenticate requests.
> **Non-STE:** The role of the middleware is to authenticate requests.

*Ref: master.md - Dictionary entry FUNCTION (n), Page 16*

---

# G

## GET (v)
- **Original:** To obtain or receive. GET THE TOOL FROM THE STORE. / Come to be. GET READY.
- **Code-domain:** To obtain or fetch. GET THE DATA FROM THE API. / To become. THE SERVICE GETS UNSTABLE UNDER LOAD.
> **STE:** Get the data from the API.
> **Non-STE:** Fetch the data from the API.

> **STE:** The service gets unstable under load.
> **Non-STE:** The service becomes unstable under load.

*Ref: master.md - Dictionary entry GET (v), Page 17*

---

## GIVE (v)
- **Original:** To provide. THIS SECTION GIVES THE CLEANING PROCEDURES FOR THE DISASSEMBLED PARTS.
- **Code-domain:** To provide or yield. THIS SECTION GIVES THE BUILD INSTRUCTIONS FOR THE MODULE.
> **STE:** This section gives the build instructions for the module.
> **Non-STE:** This section provides the build instructions for the module.

*Ref: master.md - Dictionary entry GIVE (v), Page 17*

---

## GO (v)
- **Original:** To move or travel. GO TO THE NEXT STEP.
- **Code-domain:** To proceed. GO TO THE NEXT PHASE OF THE PIPELINE.
> **STE:** Go to the next phase of the pipeline.
> **Non-STE:** Proceed to the next phase of the pipeline.

*Ref: master.md - Dictionary entry GO (v), Page 17*

---

## GOOD (adj)
- **Original:** Satisfactory. GOOD RESULTS.
- **Code-domain:** Satisfactory. GOOD TEST COVERAGE.
> **STE:** Good test coverage.
> **Non-STE:** Satisfactory test coverage.

*Ref: master.md - Dictionary entry GOOD (adj)*

---

## GROUP (n), GROUP (v)
- **Original:** A number of related items. A GROUP OF COMPONENTS. / To put into groups. GROUP THE ITEMS BY SIZE.
- **Code-domain:** A number of related items. A GROUP OF FUNCTIONS. / To organize. GROUP THE TESTS BY MODULE.
> **STE:** Group the tests by module.
> **Non-STE:** Organize the tests by module.

*Ref: master.md - Dictionary entry GROUP (n)*

---

# H

## HANDLE (v) - UNNAPROVED
- **Original:** Not approved; use TOUCH (v), OPERATE (v), USE (v).
- **Code-domain:** PROCESS (v), MANAGE (v). PROCESS THE EXCEPTION. / MANAGE THE REQUEST.
> **STE:** Process the exception.
> **Non-STE:** Handle the exception.

> **Note:** HANDLE may be a technical verb (TV) in event-driven code per Rule 1.12.

*Ref: master.md - Dictionary entry handle (v), Page 17*

---

## HAPPEN (v) - UNNAPROVED
- **Original:** OCCUR (v). AN ERROR OCCURRED DURING BUILD.
- **Code-domain:** OCCUR (v). AN EXCEPTION OCCURRED DURING INITIALIZATION.
> **STE:** An exception occurred during initialization.
> **Non-STE:** An exception happened during initialization.

*Ref: master.md - Dictionary entry happen (v)*

---

## HARD (adj)
- **Original:** Not soft; difficult. A HARD SURFACE.
- **Code-domain:** Difficult. A HARD LIMIT.
> **STE:** A hard limit on the number of connections.
> **Non-STE:** A strict limit on the number of connections.

*Ref: master.md - Dictionary entry HARD (adj)*

---

## HAVE (v)
- **Original:** To own or possess. THE UNIT HAS TWO CONNECTORS.
- **Code-domain:** To possess or contain. THE CLASS HAS TWO METHODS.
> **STE:** The class has two methods.
> **Non-STE:** The class contains two methods.

*Ref: master.md - Dictionary entry HAVE (v), Page 17*

---

## HEAD (n)
- **Original:** The top or front part. THE HEAD OF THE BOLT.
- **Code-domain:** The top or leading element. THE HEAD OF THE QUEUE.
> **STE:** The head of the queue.
> **Non-STE:** The front of the queue.

*Ref: master.md - Dictionary entry HEAD (n)*

---

## HELP (n), HELP (v)
- **Original:** Aid or assistance. GET HELP. / To give assistance. THIS MANUAL HELPS YOU TO DO THE PROCEDURE.
- **Code-domain:** Aid or assistance. GET HELP FROM THE DOCS. / To assist. THIS README HELPS YOU TO SET UP THE PROJECT.
> **STE:** This README helps you to set up the project.
> **Non-STE:** This README assists you in setting up the project.

*Ref: master.md - Dictionary entry HELP (v)*

---

## HIGH (adj)
- **Original:** Large in vertical dimension or intensity. HIGH PRESSURE.
- **Code-domain:** Large in magnitude. HIGH LOAD.
> **STE:** High load on the server.
> **Non-STE:** Heavy load on the server.

*Ref: master.md - Dictionary entry HIGH (adj)*

---

## HIT (v)
- **Original:** To strike. DO NOT HIT THE SURFACE.
- **Code-domain:** To access or collide. HIT THE ENDPOINT WITH A GET REQUEST.
> **STE:** Hit the endpoint with a GET request.
> **Non-STE:** Send a GET request to the endpoint.

*Ref: master.md - Dictionary entry HIT (v)*

---

## HOLD (v)
- **Original:** To keep in position. HOLD THE COMPONENT IN POSITION.
- **Code-domain:** To keep in state. HOLD THE LOCK UNTIL THE OPERATION COMPLETES.
> **STE:** Hold the lock until the operation completes.
> **Non-STE:** Keep the lock until the operation completes.

*Ref: master.md - Dictionary entry HOLD (v), Page 138*

---

## HOOK (n) - (TN)
- **Original:** A curved piece of metal. Code-domain: An interception point in a framework.
- **Code-domain:** A callback or interception mechanism. USE A PRE-COMMIT HOOK TO VALIDATE THE CODE.
> **STE:** Use a pre-commit hook to validate the code.
> **Non-STE:** Use a pre-commit script to validate the code.

*Ref: Code-domain technical noun*

---

## HOW (adv)
- **Original:** In what manner. HOW TO INSTALL THE COMPONENT.
- **Code-domain:** In what manner. HOW TO COMPILE THE PROJECT.
> **STE:** How to compile the project.
> **Non-STE:** Instructions to compile the project.

*Ref: master.md - Dictionary entry HOW (adv)*

---

# I

## IDENTIFY (v)
- **Original:** To find and recognize. IDENTIFY THE CAUSE OF THE PROBLEM.
- **Code-domain:** To find and recognize. IDENTIFY THE SOURCE OF THE MEMORY LEAK.
> **STE:** Identify the source of the memory leak.
> **Non-STE:** Find the source of the memory leak.

*Ref: master.md - Dictionary entry IDENTIFY (v)*

---

## IF (conj)
- **Original:** Function word that shows condition. IF THE PRESSURE IS MORE THAN THE LIMIT, STOP THE PUMP.
- **Code-domain:** Function word that shows condition. IF THE STATUS CODE IS 500, RETRY THE REQUEST.
> **STE:** If the status code is 500, retry the request.
> **Non-STE:** In the event of a 500 status code, retry the request.

*Ref: master.md - Dictionary entry IF (conj)*

---

## IGNORE (v)
- **Original:** To not pay attention to. IGNORE THE INITIAL READING.
- **Code-domain:** To not process or include. IGNORE THE CASE SENSITIVITY.
> **STE:** Ignore the case sensitivity.
> **Non-STE:** Do not consider the case sensitivity.

*Ref: master.md - Dictionary entry IGNORE (v), Page 17*

---

## IMMEDIATELY (adv)
- **Original:** Without delay. GET MEDICAL AID IMMEDIATELY.
- **Code-domain:** Without delay. RESTART THE SERVICE IMMEDIATELY.
> **STE:** Restart the service immediately.
> **Non-STE:** Restart the service right away.

*Ref: master.md - Dictionary entry IMMEDIATELY (adv), Page 18*

---

## IMPLEMENT (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To write code that fulfills a specification. IMPLEMENT THE INTERFACE.
> **STE:** Implement the interface.
> **Non-STE:** Code the interface.

*Ref: Code-domain technical verb*

---

## IMPORT (v) - (TV)
- **Original:** Not in original STE (bring goods from abroad). Code-domain: To include code from another module.
- **Code-domain:** To bring code into scope. IMPORT THE MODULE AT THE TOP OF THE FILE.
> **STE:** Import the module at the top of the file.
> **Non-STE:** Include the module at the top of the file.

*Ref: Code-domain technical verb*

---

## IMPORTANT (adj)
- **Original:** Having great significance. IMPORTANT PROCEDURE.
- **Code-domain:** Having great significance. IMPORTANT SECURITY NOTE.
> **STE:** Important security note.
> **Non-STE:** Critical security note.

*Ref: master.md - Dictionary entry IMPORTANT (adj)*

---

## IN (prep)
- **Original:** Function word that shows location or inclusion. IN THE CONTAINER.
- **Code-domain:** Function word that shows location or containment. IN THE DIRECTORY.
> **STE:** In the directory `src/lib/`.
> **Non-STE:** Within the directory `src/lib/`.

*Ref: master.md - Dictionary entry IN (prep), Page 18*

---

## INCLUDE (v)
- **Original:** To contain as part of a whole. THE KIT INCLUDES THE TOOLS.
- **Code-domain:** To contain as part of a whole. THE PACKAGE INCLUDES THE DEPENDENCIES.
> **STE:** The package includes the dependencies.
> **Non-STE:** The package contains the dependencies.

*Ref: master.md - Dictionary entry INCLUDE (v)*

---

## INCORRECT (adj)
- **Original:** Not correct. INCORRECT VALUES.
- **Code-domain:** Not correct. INCORRECT SYNTAX.
> **STE:** Incorrect syntax.
> **Non-STE:** Wrong syntax.

*Ref: master.md - Dictionary entry INCORRECT (adj)*

---

## INCREASE (v)
- **Original:** To become larger. INCREASE THE PRESSURE.
- **Code-domain:** To become larger. INCREASE THE BUFFER SIZE.
> **STE:** Increase the buffer size.
> **Non-STE:** Make the buffer larger.

*Ref: master.md - Dictionary entry INCREASE (v)*

---

## INDEX (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A numerical position in a collection. THE INDEX OF THE ELEMENT IS 0.
> **STE:** The index of the element is 0.
> **Non-STE:** The position of the element is 0.

*Ref: Code-domain technical noun*

---

## INDICATE (v) - UNNAPROVED
- **Original:** SHOW (v), SPECIFIED (adj). THE INDICATOR SHOWS THE LEVEL.
- **Code-domain:** SHOW (v). THE LOG SHOWS THE ERROR TYPE.
> **STE:** The log shows the error type.
> **Non-STE:** The log indicates the error type.

*Ref: master.md - Dictionary entry indicate (v), Page 18*

---

## INITIALIZE (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To set a starting value. INITIALIZE THE VARIABLE TO ZERO.
> **STE:** Initialize the variable to zero.
> **Non-STE:** Set the variable to zero initially.

*Ref: Code-domain technical verb*

---

## INPUT (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** Data entered into a system. VALIDATE THE USER INPUT.
> **STE:** Validate the user input.
> **Non-STE:** Validate the data entered by the user.

*Ref: Code-domain technical noun*

---

## INSERT (v) - UNNAPROVED
- **Original:** PUT (v). PUT THE COMPONENT INTO THE SLOT.
- **Code-domain:** PUT (v), ADD (v). PUT THE RECORD INTO THE DATABASE.
> **STE:** Put the record into the database.
> **Non-STE:** Insert the record into the database.

> **Note:** INSERT may be a technical verb (TV) for database operations per Rule 1.12.

*Ref: master.md - Dictionary entry insert (v), Page 146*

---

## INSPECT (v) - UNNAPROVED
- **Original:** EXAMINE (v), CHECK (v). EXAMINE THE COMPONENT FOR DAMAGE.
- **Code-domain:** EXAMINE (v), REVIEW (v). REVIEW THE CODE FOR VULNERABILITIES.
> **STE:** Review the code for vulnerabilities.
> **Non-STE:** Inspect the code for vulnerabilities.

*Ref: master.md - Dictionary entry inspect (v)*

---

## INSTALL (v)
- **Original:** To put into position for use. INSTALL THE COMPONENT IN THE RACK.
- **Code-domain:** To set up software for use. INSTALL THE PACKAGE WITH NPM.
> **STE:** Install the package with npm.
> **Non-STE:** Set up the package with npm.

*Ref: master.md - Dictionary entry INSTALL (v)*

---

## INSTRUCTION (n)
- **Original:** A direction for action. OBEY THE INSTRUCTIONS IN THE MANUAL.
- **Code-domain:** A direction for action. OBEY THE INSTRUCTIONS IN THE README.
> **STE:** Obey the instructions in the README.
> **Non-STE:** Follow the instructions in the README.

*Ref: master.md - Dictionary entry INSTRUCTION (n)*

---

## INTERFACE (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A contract defining methods a class must implement. THE INTERFACE DEFINES THREE METHODS.
> **STE:** The interface defines three methods.
> **Non-STE:** The contract defines three methods.

*Ref: Code-domain technical noun*

---

## INVALID (adj) - (TN)
- **Original:** Not in original STE. Code-domain technical adjective.
- **Code-domain:** Not valid or acceptable. AN INVALID TOKEN.
> **STE:** An invalid token.
> **Non-STE:** A bad token.

*Ref: Code-domain technical adjective*

---

## ISOLATE (v)
- **Original:** To separate from others. ISOLATE THE SYSTEM.
- **Code-domain:** To separate for testing or security. ISOLATE THE COMPONENT FOR UNIT TESTING.
> **STE:** Isolate the component for unit testing.
> **Non-STE:** Separate the component for unit testing.

*Ref: master.md - Dictionary entry ISOLATE (v)*

---

## IT (pron)
- **Original:** A pronoun for a thing. THE COMPONENT. IT IS INSTALLED IN THE RACK.
- **Code-domain:** A pronoun for a thing. THE PACKAGE. IT IS IN THE REGISTRY.
> **STE:** The package. It is in the registry.
> **Non-STE:** The package is in the registry.

*Ref: master.md - Dictionary entry IT (pron), Page 18*

---

# J

## JOIN (v)
- **Original:** To connect. JOIN THE TWO PIPES.
- **Code-domain:** To concatenate or merge. JOIN THE TWO STRINGS.
> **STE:** Join the two strings.
> **Non-STE:** Concatenate the two strings.

*Ref: master.md - Dictionary entry JOIN (v)*

---

# K

## KEEP (v)
- **Original:** To continue to have. KEEP THE PART IN A DRY AREA.
- **Code-domain:** To maintain state. KEEP THE CONNECTION OPEN.
> **STE:** Keep the connection open.
> **Non-STE:** Maintain the connection.

*Ref: master.md - Dictionary entry KEEP (v)*

---

## KEY (n) - (TN)
- **Original:** A piece of metal for locks. Code-domain: An identifier for data access.
- **Code-domain:** A unique identifier. THE KEY FOR THE CACHE ENTRY IS THE USER ID.
> **STE:** The key for the cache entry is the user ID.
> **Non-STE:** The identifier for the cache entry is the user ID.

*Ref: Code-domain technical noun*

---

## KILL (v)
- **Original:** To cause to die. Code-domain adaptation: To terminate a process.
- **Code-domain:** To force-terminate a process. KILL THE PROCESS WITH SIGTERM.
> **STE:** Kill the process with SIGTERM.
> **Non-STE:** Terminate the process with SIGTERM.

*Ref: master.md - Dictionary entry KILL (v)*

---

## KNOW (v)
- **Original:** To be aware. YOU MUST KNOW THE SPECIFICATION.
- **Code-domain:** To understand. YOU MUST KNOW THE API SPECIFICATION.
> **STE:** You must know the API specification.
> **Non-STE:** You must be familiar with the API specification.

*Ref: master.md - Dictionary entry KNOW (v)*

---

# L

## LARGE (adj)
- **Original:** Big in size or quantity. LARGE QUANTITY.
- **Code-domain:** Big in size or quantity. LARGE DATASET.
> **STE:** A large dataset.
> **Non-STE:** A big dataset.

*Ref: master.md - Dictionary entry LARGE (adj)*

---

## LAST (adj), LAST (adv)
- **Original:** After all others. THE LAST STEP. / After all others. DO THIS STEP LAST.
- **Code-domain:** After all others. THE LAST ITERATION. / EXECUTE THE TEARDOWN LAST.
> **STE:** Execute the teardown last.
> **Non-STE:** Execute the teardown at the end.

*Ref: master.md - Dictionary entry LAST (adj)*

---

## LAYER (n) - (TN)
- **Original:** A thickness of material. Code-domain: A level in an architecture.
- **Code-domain:** A logical level in a stack. THE DATA ACCESS LAYER HANDLES QUERIES.
> **STE:** The data access layer handles queries.
> **Non-STE:** The data tier handles queries.

*Ref: Code-domain technical noun*

---

## LEFT (adj), LEFT (adv)
- **Original:** In a direction opposite to right. THE LEFT SIDE. / MOVE THE LEVER LEFT.
- **Code-domain:** In a direction opposite to right. THE LEFT PANEL. / ALIGN THE TEXT LEFT.
> **STE:** Align the text left.
> **Non-STE:** Align the text to the left.

*Ref: master.md - Dictionary entry LEFT (adj)*

---

## LENGTH (n)
- **Original:** The measurement from end to end. MEASURE THE LENGTH.
- **Code-domain:** The number of elements. THE LENGTH OF THE ARRAY IS 10.
> **STE:** The length of the array is 10.
> **Non-STE:** The array has 10 elements.

*Ref: master.md - Dictionary entry LENGTH (n)*

---

## LESS (adj), LESS (adv), LESS (prep)
- **Original:** Smaller in quantity. LESS FUEL. / To a smaller degree. LESS OFTEN. / Minus. 15 LESS 10 IS 5.
- **Code-domain:** Smaller in quantity. LESS MEMORY. / To a smaller degree. LESS FREQUENTLY.
> **STE:** Less memory usage.
> **Non-STE:** Lower memory usage.

*Ref: master.md - Dictionary entry LESS (prep), Page 18*

---

## LET (v)
- **Original:** To permit or allow. LET THE ENGINE COOL.
- **Code-domain:** To permit or bind. LET THE VARIABLE BE MUTABLE.
> **STE:** Let the process complete before you restart.
> **Non-STE:** Allow the process to complete before you restart.

*Ref: master.md - Dictionary entry LET (v), Page 18*

---

## LEVEL (n)
- **Original:** A relative position or height. THE OIL LEVEL.
- **Code-domain:** A degree or rank. THE LOG LEVEL.
> **STE:** Set the log level to debug.
> **Non-STE:** Set the logging severity to debug.

*Ref: master.md - Dictionary entry LEVEL (n)*

---

## LIBRARY (n) - (TN)
- **Original:** A collection of books. Code-domain: A collection of reusable code.
- **Code-domain:** A package of reusable code. IMPORT THE STANDARD LIBRARY.
> **STE:** Import the standard library.
> **Non-STE:** Include the standard library.

*Ref: Code-domain technical noun*

---

## LIFT (v)
- **Original:** To raise. LIFT THE COMPONENT.
- **Code-domain:** To promote or extract. LIFT THE FUNCTION TO A SEPARATE MODULE.
> **STE:** Lift the function to a separate module.
> **Non-STE:** Extract the function to a separate module.

*Ref: master.md - Dictionary entry LIFT (v)*

---

## LIGHT (adj)
- **Original:** Not heavy; not dark. LIGHT FORCE. / LIGHT COLOR.
- **Code-domain:** Not heavy in resource usage. LIGHT PROCESS. / Not dark. LIGHT THEME.
> **STE:** A light process with small memory footprint.
> **Non-STE:** A lightweight process.

*Ref: master.md - Dictionary entry LIGHT (adj), Page 18*

---

## LIMIT (n), LIMIT (v)
- **Original:** A boundary or maximum. THE SPEED LIMIT. / To restrict. LIMIT THE FLOW.
- **Code-domain:** A boundary or maximum. THE RATE LIMIT. / To restrict. LIMIT THE NUMBER OF REQUESTS.
> **STE:** Limit the number of requests.
> **Non-STE:** Restrict the number of requests.

*Ref: master.md - Dictionary entry LIMIT (n)*

---

## LINE (n)
- **Original:** A long thin mark. A STRAIGHT LINE.
- **Code-domain:** A row of text in a file. THE ERROR IS AT LINE 42. / A connection. THE TRANSMISSION LINE.
> **STE:** The error is at line 42.
> **Non-STE:** The error is on line 42.

*Ref: master.md - Dictionary entry LINE (n)*

---

## LINK (n), LINK (v)
- **Original:** A connection. / To connect. LINK THE TWO COMPONENTS.
- **Code-domain:** A reference or URL. THE LINK TO THE DOCUMENTATION. / To connect. LINK THE LIBRARY TO THE PROJECT.
> **STE:** Link the library to the project.
> **Non-STE:** Connect the library to the project.

*Ref: master.md - Dictionary entry LINK (n)*

---

## LIST (n), LIST (v)
- **Original:** A series of items. / To give as a list. LIST THE COMPONENTS.
- **Code-domain:** A data structure. A LINKED LIST. / To enumerate. LIST THE FILES IN THE DIRECTORY.
> **STE:** List the files in the directory.
> **Non-STE:** Show the files in the directory.

*Ref: master.md - Dictionary entry LIST (n)*

---

## LOAD (n), LOAD (v)
- **Original:** A weight. / To put a load on or into. LOAD THE SOFTWARE.
- **Code-domain:** Demand on a system. THE SERVER LOAD. / To bring data into memory. LOAD THE CONFIGURATION FILE.
> **STE:** Load the configuration file.
> **Non-STE:** Read the configuration file.

*Ref: master.md - Dictionary entry LOAD (n)*

---

## LOCATE (v) - UNNAPROVED
- **Original:** FIND (v). FIND THE COMPONENT.
- **Code-domain:** FIND (v). FIND THE ERROR IN THE LOGS.
> **STE:** Find the error in the logs.
> **Non-STE:** Locate the error in the logs.

*Ref: master.md - Dictionary entry locate (v), Page 18*

---

## LOCK (v)
- **Original:** To secure with a lock. LOCK THE DOOR.
- **Code-domain:** To prevent concurrent access. LOCK THE MUTEX.
> **STE:** Lock the mutex.
> **Non-STE:** Acquire the mutex.

*Ref: master.md - Dictionary entry LOCK (v), Page 18*

---

## LOG (n), LOG (v) - (TN/TV)
- **Original:** A record of events (not in original STE nautical sense). Code-domain.
- **Code-domain:** A record of system events. READ THE LOG FILE. / To record. LOG THE ERROR.
> **STE:** Log the error to the file.
> **Non-STE:** Write the error to the file.

*Ref: Code-domain technical noun/verb*

---

## LONG (adj)
- **Original:** Having large length. A LONG CABLE.
- **Code-domain:** Having large length or duration. A LONG PROCESS.
> **STE:** A long process.
> **Non-STE:** A time-consuming process.

*Ref: master.md - Dictionary entry LONG (adj), Page 18*

---

## LOOK (v)
- **Original:** To direct eyes toward. LOOK AT THE INDICATOR.
- **Code-domain:** To examine. LOOK AT THE ERROR MESSAGE.
> **STE:** Look at the error message.
> **Non-STE:** Examine the error message.

*Ref: master.md - Dictionary entry LOOK (v)*

---

## LOOP (n) - (TN)
- **Original:** A curved shape. Code-domain: A repeating code block.
- **Code-domain:** A control structure that repeats. THE FOR LOOP ITERATES 10 TIMES.
> **STE:** The for loop iterates 10 times.
> **Non-STE:** The iteration runs 10 times.

*Ref: Code-domain technical noun*

---

## LOOSE (adj)
- **Original:** Not tight. A LOOSE CONNECTION.
- **Code-domain:** Not tightly coupled. LOOSE COUPLING BETWEEN MODULES.
> **STE:** Loose coupling between modules.
> **Non-STE:** Decoupled modules.

*Ref: master.md - Dictionary entry LOOSE (adj), Page 18*

---

## LOW (adj)
- **Original:** Small in height or intensity. LOW PRESSURE.
- **Code-domain:** Small in magnitude. LOW LATENCY.
> **STE:** Low latency.
> **Non-STE:** Minimal delay.

*Ref: master.md - Dictionary entry LOW (adj)*

---

## LOWER (v)
- **Original:** To move something down. LOWER THE COMPONENT.
- **Code-domain:** To reduce. LOWER THE LOG LEVEL.
> **STE:** Lower the log level.
> **Non-STE:** Reduce the log level.

*Ref: master.md - Dictionary entry LOWER (v)*

---

# M

## MAIN (adj) - UNNAPROVED
- **Original:** PRIMARY (adj). THE PRIMARY CAUSE OF VALVE FAILURE IS CONTAMINATION OF THE FLUID.
- **Code-domain:** PRIMARY (adj). THE PRIMARY CAUSE OF THE CRASH IS A NULL POINTER.
> **STE:** The primary cause of the crash is a null pointer.
> **Non-STE:** The main cause of the crash is a null pointer.

*Ref: master.md - Dictionary entry main (adj), Page 18, 132, 146*

---

## MAKE (v)
- **Original:** To create or cause. MAKE A HOLE.
- **Code-domain:** To create or cause. MAKE A COPY OF THE FILE.
> **STE:** Make a copy of the file.
> **Non-STE:** Create a copy of the file.

*Ref: master.md - Dictionary entry MAKE (v)*

---

## MAKE SURE (v)
- **Original:** To verify or confirm. MAKE SURE THAT THE VALVE IS CLOSED.
- **Code-domain:** To verify. MAKE SURE THAT THE TESTS PASS.
> **STE:** Make sure that the tests pass.
> **Non-STE:** Ensure that the tests pass.

*Ref: master.md - Dictionary entry MAKE SURE (v)*

---

## MANAGE (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb (e.g., package manager, state manager).
- **Code-domain:** To control or administer. THE PACKAGE MANAGER MANAGES DEPENDENCIES.
> **STE:** The package manager manages dependencies.
> **Non-STE:** The package manager handles dependencies.

*Ref: Code-domain technical verb*

---

## MANDATORY (adj)
- **Original:** Compulsory. IT IS MANDATORY TO OBEY THE SAFETY INSTRUCTIONS.
- **Code-domain:** Required, not optional. THE API KEY IS MANDATORY.
> **STE:** The API key is mandatory.
> **Non-STE:** The API key is required.

*Ref: master.md - Dictionary entry MANDATORY (adj), Page 18*

---

## MANUAL (adj), MANUAL (n)
- **Original:** Done by hand (not automatic). MANUAL OPERATION. / A book. READ THE MANUAL.
- **Code-domain:** Done by human (not automated). MANUAL REVIEW. / A document. READ THE MANUAL.
> **STE:** Manual review of the code.
> **Non-STE:** Human review of the code.

> **STE:** Read the manual before you start.
> **Non-STE:** Read the docs before you start.

*Ref: master.md - Dictionary entry MANUAL (adj), Page 19*

---

## MANY (adj)
- **Original:** A large number. MANY COMPONENTS.
- **Code-domain:** A large number. MANY REQUESTS.
> **STE:** Many requests per second.
> **Non-STE:** Numerous requests per second.

*Ref: master.md - Dictionary entry MANY (adj), Page 19*

---

## MAP (v) - (TV)
- **Original:** To make a representation (cartography). Code-domain: To transform data.
- **Code-domain:** To transform each element. MAP THE ARRAY TO UPPERCASE.
> **STE:** Map the array to uppercase.
> **Non-STE:** Transform each element of the array.

*Ref: Code-domain technical verb*

---

## MARK (n), MARK (v)
- **Original:** A visible sign. A REFERENCE MARK. / To make a mark. MARK THE POSITION.
- **Code-domain:** A visible sign. A BENCHMARK. / To flag. MARK THE FUNCTION AS DEPRECATED.
> **STE:** Mark the function as deprecated.
> **Non-STE:** Flag the function as deprecated.

*Ref: master.md - Dictionary entry MARK (n)*

---

## MATCH (v)
- **Original:** To be the same or fit together. THE PARTS MUST MATCH.
- **Code-domain:** To correspond. THE PATTERN MUST MATCH THE INPUT.
> **STE:** The pattern must match the input.
> **Non-STE:** The pattern must correspond to the input.

*Ref: master.md - Dictionary entry MATCH (v)*

---

## MATERIAL (n)
- **Original:** Substance. THE MATERIAL IS RESISTANT TO HEAT.
- **Code-domain:** Reference material. REFER TO THE TRAINING MATERIAL.
> **STE:** Refer to the training material.
> **Non-STE:** Refer to the training resources.

*Ref: master.md - Dictionary entry MATERIAL (n), Page 19*

---

## MAXIMUM (adj), MAXIMUM (n)
- **Original:** The greatest possible. MAXIMUM SPEED. / The greatest possible quantity. THE MAXIMUM IS 100.
- **Code-domain:** The greatest possible. MAXIMUM CONNECTIONS. / The greatest possible quantity. THE MAXIMUM IS 100.
> **STE:** Maximum connections is 100.
> **Non-STE:** The limit is 100 connections.

*Ref: master.md - Dictionary entry MAXIMUM (adj)*

---

## MEASURE (v)
- **Original:** To find the size or quantity. MEASURE THE DISTANCE.
- **Code-domain:** To quantify metrics. MEASURE THE RESPONSE TIME.
> **STE:** Measure the response time.
> **Non-STE:** Calculate the response time.

*Ref: master.md - Dictionary entry MEASURE (v), Page 20*

---

## MEMORY (n) - (TN)
- **Original:** The faculty of remembering. Code-domain: Computer storage.
- **Code-domain:** A system's working storage. THE APPLICATION USES 256 MB OF MEMORY.
> **STE:** The application uses 256 MB of memory.
> **Non-STE:** The application uses 256 MB of RAM.

*Ref: Code-domain technical noun*

---

## MERGE (v) - (TV)
- **Original:** To combine. MERGE THE TWO LISTS.
- **Code-domain:** To combine branches. MERGE THE FEATURE BRANCH INTO MAIN.
> **STE:** Merge the feature branch into main.
> **Non-STE:** Combine the feature branch into main.

*Ref: Code-domain technical verb*

---

## MESSAGE (n)
- **Original:** A communication. SEND A MESSAGE.
- **Code-domain:** A unit of communication. THE ERROR MESSAGE DESCRIBES THE ISSUE.
> **STE:** The error message describes the issue.
> **Non-STE:** The error text describes the issue.

*Ref: master.md - Dictionary entry MESSAGE (n)*

---

## METHOD (n) - (TN)
- **Original:** A way of doing something. THE METHOD OF INSTALLATION.
- **Code-domain:** A function within a class. THE METHOD TAKES TWO PARAMETERS.
> **STE:** The method takes two parameters.
> **Non-STE:** The function takes two parameters.

*Ref: Code-domain technical noun*

---

## MINIMUM (adj), MINIMUM (n)
- **Original:** The smallest possible. MINIMUM PRESSURE. / The smallest possible quantity. THE MINIMUM IS 5.
- **Code-domain:** The smallest possible. MINIMUM PASSWORD LENGTH. / The smallest possible quantity. THE MINIMUM IS 8.
> **STE:** The minimum password length is 8.
> **Non-STE:** The password must be at least 8 characters.

*Ref: master.md - Dictionary entry MINIMUM (adj), Page 19*

---

## MINUS (prep)
- **Original:** With the subtraction of. 10 MINUS 3 IS 7.
- **Code-domain:** Mathematical subtraction. THE VALUE IS TOTAL MINUS OVERHEAD.
> **STE:** The value is total minus overhead.
> **Non-STE:** The value is total less overhead.

*Ref: master.md - Dictionary entry MINUS (prep), Page 19*

---

## MISSING (adj)
- **Original:** Not present. A MISSING COMPONENT.
- **Code-domain:** Not present. A MISSING DEPENDENCY.
> **STE:** A missing dependency.
> **Non-STE:** A dependency that is not installed.

*Ref: master.md - Dictionary entry MISSING (adj)*

---

## MIX (v)
- **Original:** To combine two or more substances. MIX THE COMPOUND.
- **Code-domain:** To combine. MIX CONCERNS IN A SINGLE MODULE.
> **STE:** Do not mix concerns in a single module.
> **Non-STE:** Do not combine concerns in a single module.

*Ref: master.md - Dictionary entry MIX (v), Page 19*

---

## MODE (n) - (TN)
- **Original:** A way of operating. THE AUTOPILOT MODE.
- **Code-domain:** A state of operation. THE DEBUG MODE SHOWS MORE INFORMATION.
> **STE:** The debug mode shows more information.
> **Non-STE:** Debug builds show more information.

*Ref: Code-domain technical noun*

---

## MODEL (n) - (TN)
- **Original:** A representation. Code-domain: A data structure or ML artifact.
- **Code-domain:** A data structure or machine learning artifact. THE USER MODEL HAS THREE FIELDS. / TRAIN THE MODEL.
> **STE:** The user model has three fields.
> **Non-STE:** The user schema has three fields.

*Ref: Code-domain technical noun*

---

## MODIFY (v) - UNNAPROVED
- **Original:** CHANGE (v), MODIFICATION (TN). MAKE CHANGES TO THE CONFIGURATION.
- **Code-domain:** CHANGE (v). CHANGE THE FILE PERMISSIONS.
> **STE:** Change the file permissions.
> **Non-STE:** Modify the file permissions.

*Ref: master.md - Dictionary entry modify (v), Page 19*

---

## MODULE (n) - (TN)
- **Original:** A self-contained unit. Code-domain: A self-contained code unit.
- **Code-domain:** An independent unit of code. EACH MODULE HAS ITS OWN NAMESPACE.
> **STE:** Each module has its own namespace.
> **Non-STE:** Each package has its own namespace.

*Ref: Code-domain technical noun*

---

## MONITOR (v)
- **Original:** To watch or observe. MONITOR THE PRESSURE.
- **Code-domain:** To observe system behavior. MONITOR THE SERVER LOGS.
> **STE:** Monitor the server logs.
> **Non-STE:** Watch the server logs.

*Ref: master.md - Dictionary entry MONITOR (v)*

---

## MORE (adj), MORE (adv)
- **Original:** A larger quantity or degree. MORE FUEL. / MORE QUICKLY.
- **Code-domain:** A larger quantity or degree. MORE MEMORY. / MORE EFFICIENTLY.
> **STE:** More memory allocation.
> **Non-STE:** Additional memory allocation.

*Ref: master.md - Dictionary entry MORE (adj), Page 19*

---

## MOST (adj), MOST (adv)
- **Original:** The largest quantity or degree. MOST COMPONENTS. / To the greatest degree. MOST FREQUENTLY.
- **Code-domain:** The largest quantity or degree. MOST ERRORS. / MOST FREQUENTLY.
> **STE:** Most errors occur at startup.
> **Non-STE:** The majority of errors occur at startup.

*Ref: master.md - Dictionary entry MOST (adj), Page 19*

---

## MOVE (v)
- **Original:** To change position. MOVE THE LEVER.
- **Code-domain:** To transfer data or code. MOVE THE FILE TO THE ARCHIVE.
> **STE:** Move the file to the archive.
> **Non-STE:** Transfer the file to the archive.

*Ref: master.md - Dictionary entry MOVE (v)*

---

## MUCH (adj), MUCH (adv)
- **Original:** A large amount. NOT MUCH DAMAGE.
- **Code-domain:** A large amount. NOT MUCH MEMORY.
> **STE:** Not much memory usage.
> **Non-STE:** Low memory usage.

*Ref: master.md - Dictionary entry MUCH (adj)*

---

## MUST (v)
- **Original:** Verb that shows obligation or necessity. YOU MUST OBEY THE SAFETY INSTRUCTIONS.
- **Code-domain:** Verb that shows obligation or necessity. YOU MUST VALIDATE ALL INPUTS.
> **STE:** You must validate all inputs.
> **Non-STE:** You have to validate all inputs.

*Ref: master.md - Dictionary entry MUST (v), Page 19*

---

# N

## NAME (n), NAME (v)
- **Original:** A word that identifies a thing. THE NAME OF THE COMPONENT. / To give a name. NAME THE FILE.
- **Code-domain:** An identifier. THE NAME OF THE FUNCTION. / To assign an identifier. NAME THE VARIABLE `count`.
> **STE:** Name the variable `count`.
> **Non-STE:** Call the variable `count`.

*Ref: master.md - Dictionary entry NAME (n), Page 19*

---

## NEAR (adj), NEAR (prep)
- **Original:** At a short distance. THE NEAR COMPONENT. / NEAR THE DOOR.
- **Code-domain:** At a short logical distance. THE NEAR CACHE. / NEAR THE END OF THE FILE.
> **STE:** Near the end of the file.
> **Non-STE:** Close to the end of the file.

*Ref: master.md - Dictionary entry NEAR (prep), Page 19*

---

## NECESSARY (adj)
- **Original:** Needed. IT IS NECESSARY TO DO THE TEST.
- **Code-domain:** Needed. IT IS NECESSARY TO RESTART THE SERVICE.
> **STE:** It is necessary to restart the service.
> **Non-STE:** You must restart the service.

*Ref: master.md - Dictionary entry NECESSARY (adj), Page 19*

---

## NEED (v) - UNNAPROVED
- **Original:** NECESSARY (adj). IT IS NECESSARY TO CHANGE THE FILTER.
- **Code-domain:** MUST (v), NECESSARY (adj). YOU MUST INSTALL THE DEPENDENCIES.
> **STE:** You must install the dependencies.
> **Non-STE:** You need to install the dependencies.

*Ref: master.md - Dictionary entry need (v), Page 19, 146*

---

## NEVER (adv)
- **Original:** Not at any time. NEVER USE THIS TOOL WITHOUT PROTECTION.
- **Code-domain:** Not at any time. NEVER STORE PASSWORDS IN PLAIN TEXT.
> **STE:** Never store passwords in plain text.
> **Non-STE:** Do not store passwords in plain text under any circumstances.

*Ref: master.md - Dictionary entry NEVER (adv)*

---

## NEW (adj)
- **Original:** Recently made. A NEW COMPONENT.
- **Code-domain:** Recently created. A NEW INSTANCE OF THE CLASS.
> **STE:** A new instance of the class.
> **Non-STE:** A fresh instance of the class.

*Ref: master.md - Dictionary entry NEW (adj)*

---

## NEXT (adj)
- **Original:** That follows immediately. THE NEXT STEP.
- **Code-domain:** That follows immediately. THE NEXT ITERATION.
> **STE:** The next iteration.
> **Non-STE:** The following iteration.

*Ref: master.md - Dictionary entry NEXT (adj), Page 19*

---

## NO (adj)
- **Original:** Not any. NO DAMAGE.
- **Code-domain:** Not any. NO ERRORS.
> **STE:** No errors in the output.
> **Non-STE:** Zero errors in the output.

*Ref: master.md - Dictionary entry NO (adj)*

---

## NONE (pron)
- **Original:** Not one. NONE OF THE COMPONENTS ARE DAMAGED.
- **Code-domain:** Not one. NONE OF THE TESTS FAIL.
> **STE:** None of the tests fail.
> **Non-STE:** All tests pass.

*Ref: master.md - Dictionary entry NONE (pron)*

---

## NORMAL (adj) - UNNAPROVED
- **Original:** Not approved; use USUAL (adj), CORRECT (adj), SPECIFIED (adj).
- **Code-domain:** USUAL (adj). THE USUAL BEHAVIOR IS TO RETURN ZERO.
> **STE:** The usual behavior is to return zero.
> **Non-STE:** The normal behavior is to return zero.

*Ref: master.md - Dictionary entry normal (adj), Page 19*

---

## NOT (adv)
- **Original:** Function word that shows negation. DO NOT USE THIS TOOL.
- **Code-domain:** Function word that shows negation. DO NOT USE DEPRECATED FUNCTIONS.
> **STE:** Do not use deprecated functions.
> **Non-STE:** Avoid using deprecated functions.

*Ref: master.md - Dictionary entry NOT (adv), Page 19*

---

## NOTE (n), NOTE (v)
- **Original:** A short record. MAKE A NOTE. / To write. NOTE THE VALUE.
- **Code-domain:** An annotation. ADD A NOTE IN THE CODE. / To record. NOTE THE ERROR CODE.
> **STE:** Add a note in the code.
> **Non-STE:** Add a comment in the code.

*Ref: master.md - Dictionary entry NOTE (n)*

---

## NULL (adj) - (TN)
- **Original:** Not in original STE. Code-domain technical adjective.
- **Code-domain:** Having no value. THE POINTER IS NULL.
> **STE:** The pointer is null.
> **Non-STE:** The pointer is empty.

*Ref: Code-domain technical adjective*

---

## NUMBER (n)
- **Original:** A mathematical value. THE NUMBER OF COMPONENTS.
- **Code-domain:** A numeric value. THE NUMBER OF RECORDS.
> **STE:** The number of records is 100.
> **Non-STE:** The count of records is 100.

*Ref: master.md - Dictionary entry NUMBER (n)*

---

# O

## OBJECT (n) - (TN)
- **Original:** A thing. Code-domain: An instance of a class.
- **Code-domain:** An instance of a class. CREATE A NEW OBJECT OF THE USER CLASS.
> **STE:** Create a new object of the User class.
> **Non-STE:** Instantiate the User class.

*Ref: Code-domain technical noun*

---

## OBEY (v)
- **Original:** To follow instructions. OBEY THE SAFETY INSTRUCTIONS.
- **Code-domain:** To follow instructions. OBEY THE CODING STANDARDS.
> **STE:** Obey the coding standards.
> **Non-STE:** Follow the coding standards.

*Ref: master.md - Dictionary entry OBEY (v)*

---

## OCCUR (v)
- **Original:** To happen. AN ERROR OCCURRED DURING OPERATION.
- **Code-domain:** To happen. AN EXCEPTION OCCURRED AT RUNTIME.
> **STE:** An exception occurred at runtime.
> **Non-STE:** An exception was thrown at runtime.

*Ref: master.md - Dictionary entry OCCUR (v)*

---

## OF (prep)
- **Original:** Function word that shows belonging or relationship. THE NAME OF THE COMPONENT.
- **Code-domain:** Function word that shows belonging or relationship. THE NAME OF THE FUNCTION.
> **STE:** The name of the function.
> **Non-STE:** The function's name.

*Ref: master.md - Dictionary entry OF (prep)*

---

## OFF (adv), OFF (prep)
- **Original:** Not on or not operating. TURN OFF THE POWER.
- **Code-domain:** Not operating or disabled. TURN OFF THE FEATURE FLAG.
> **STE:** Turn off the feature flag.
> **Non-STE:** Disable the feature flag.

*Ref: master.md - Dictionary entry OFF (adv)*

---

## ON (adv), ON (prep)
- **Original:** In operation or in a position above. TURN ON THE POWER. / ON THE SURFACE.
- **Code-domain:** In operation or applied to. TURN ON THE DEBUG MODE. / ON THE TERMINAL.
> **STE:** Turn on the debug mode.
> **Non-STE:** Enable the debug mode.

*Ref: master.md - Dictionary entry ON (adv), Page 19*

---

## ONLY (adv)
- **Original:** And no other. ONLY THE TECHNICIAN CAN DO THIS PROCEDURE.
- **Code-domain:** Exclusively. ONLY THE ADMIN CAN RUN THIS COMMAND.
> **STE:** Only the admin can run this command.
> **Non-STE:** Solely the admin can run this command.

*Ref: master.md - Dictionary entry ONLY (adv)*

---

## OPEN (v), OPEN (adj)
- **Original:** To move so as to give access. OPEN THE DOOR. / Not closed. AN OPEN CONNECTION.
- **Code-domain:** To initiate access. OPEN THE FILE. / Accessible. AN OPEN PORT.
> **STE:** Open the file for reading.
> **Non-STE:** Read the file.

> **STE:** An open port on the firewall.
> **Non-STE:** A listening port on the firewall.

*Ref: master.md - Dictionary entry OPEN (v)*

---

## OPERATE (v)
- **Original:** To control the function of. OPERATE THE SYSTEM.
- **Code-domain:** To control or run. OPERATE THE APPLICATION.
> **STE:** Operate the application through the CLI.
> **Non-STE:** Run the application through the CLI.

*Ref: master.md - Dictionary entry OPERATE (v)*

---

## OPERATION (n)
- **Original:** An action or process. THE OPERATION OF THE SYSTEM.
- **Code-domain:** An action or process. THE OPERATION OF THE REQUEST IS ASYNCHRONOUS.
> **STE:** The operation of the request is asynchronous.
> **Non-STE:** The request is processed asynchronously.

*Ref: master.md - Dictionary entry OPERATION (n)*

---

## OPTION (n) - UNNAPROVED
- **Original:** ALTERNATIVE (n), CAN (v). YOU CAN USE AN ALTERNATIVE METHOD.
- **Code-domain:** ALTERNATIVE (n), CAN (v). YOU CAN USE AN ALTERNATIVE CONFIGURATION.
> **STE:** You can use an alternative configuration.
> **Non-STE:** You have the option to use another configuration.

*Ref: master.md - Dictionary entry option (n), Page 20*

---

## OR (conj)
- **Original:** Function word that shows alternatives. USE TOOL A OR TOOL B.
- **Code-domain:** Function word that shows alternatives. USE PYTHON OR NODE.JS.
> **STE:** Use Python or Node.js.
> **Non-STE:** Use Python; alternatively use Node.js.

*Ref: master.md - Dictionary entry OR (conj)*

---

## ORDER (n)
- **Original:** A sequence. IN THE CORRECT ORDER.
- **Code-domain:** A sequence. EXECUTE THE STEPS IN THE GIVEN ORDER.
> **STE:** Execute the steps in the given order.
> **Non-STE:** Execute the steps sequentially.

*Ref: master.md - Dictionary entry ORDER (n)*

---

## OTHER (adj)
- **Original:** Different from the one specified. THE OTHER COMPONENT.
- **Code-domain:** Different from the one specified. THE OTHER ENDPOINT.
> **STE:** The other endpoint returns JSON.
> **Non-STE:** The alternative endpoint returns JSON.

*Ref: master.md - Dictionary entry OTHER (adj)*

---

## OUTPUT (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** Data produced by a program. THE OUTPUT OF THE COMMAND IS A LIST.
> **STE:** The output of the command is a list.
> **Non-STE:** The command prints a list.

*Ref: Code-domain technical noun*

---

## OVER (prep) - UNNAPROVED
- **Original:** MORE THAN, ABOVE, ON. MORE THAN THE LIMIT.
- **Code-domain:** MORE THAN, ABOVE. MORE THAN THE THRESHOLD.
> **STE:** More than the threshold.
> **Non-STE:** Over the threshold.

*Ref: master.md - Dictionary entry over (prep), Page 20, 146*

---

## OVERRIDE (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To replace a method in a subclass. OVERRIDE THE DEFAULT BEHAVIOR.
> **STE:** Override the default behavior in the subclass.
> **Non-STE:** Replace the default behavior in the subclass.

*Ref: Code-domain technical verb*

---

# P

## PACKAGE (n) - (TN)
- **Original:** A bundle. Code-domain: A distributable unit of software.
- **Code-domain:** A distributable unit of software. INSTALL THE PACKAGE WITH PIP.
> **STE:** Install the package with pip.
> **Non-STE:** Install the library with pip.

*Ref: Code-domain technical noun*

---

## PAGE (n)
- **Original:** A sheet. A PAGE OF THE MANUAL.
- **Code-domain:** A view or screen. THE LANDING PAGE OF THE APPLICATION.
> **STE:** The landing page of the application.
> **Non-STE:** The home screen of the application.

*Ref: master.md - Dictionary entry PAGE (n)*

---

## PARAMETER (n) - (TN)
- **Original:** A defining characteristic. Code-domain: A variable in a function signature.
- **Code-domain:** A variable passed to a function. THE FUNCTION TAKES TWO PARAMETERS.
> **STE:** The function takes two parameters.
> **Non-STE:** The function accepts two arguments.

*Ref: Code-domain technical noun*

---

## PART (n)
- **Original:** A piece of a whole. A PART OF THE UNIT.
- **Code-domain:** A section. A PART OF THE DOCUMENTATION.
> **STE:** A part of the documentation.
> **Non-STE:** A section of the documentation.

*Ref: master.md - Dictionary entry PART (n), Page 20*

---

## PASS (v)
- **Original:** To go past or succeed. PASS THE TOOL THROUGH THE HOLE.
- **Code-domain:** To succeed in a test. THE TEST PASSES.
> **STE:** The test passes.
> **Non-STE:** The test succeeds.

*Ref: master.md - Dictionary entry PASS (v)*

---

## PASTE (v)
- **Original:** Not in original STE (adhesive). Code-domain: To insert copied data.
- **Code-domain:** To insert copied content. PASTE THE TEXT INTO THE EDITOR.
> **STE:** Paste the text into the editor.
> **Non-STE:** Insert the copied text into the editor.

*Ref: Code-domain technical verb*

---

## PATH (n) - (TN)
- **Original:** A route. Code-domain: A filesystem location.
- **Code-domain:** A filesystem location. THE PATH TO THE CONFIG FILE.
> **STE:** The path to the config file is `/etc/app/`.
> **Non-STE:** The location of the config file is `/etc/app/`.

*Ref: Code-domain technical noun*

---

## PATTERN (n) - (TN)
- **Original:** A repeated design. Code-domain: A regex or design pattern.
- **Code-domain:** A reusable design or matching expression. THE REGEX PATTERN MATCHES THE INPUT.
> **STE:** The regex pattern matches the input.
> **Non-STE:** The regular expression matches the input.

*Ref: Code-domain technical noun*

---

## PERFORM (v) - UNNAPROVED
- **Original:** DO (v). DO THE TEST.
- **Code-domain:** DO (v). DO THE BUILD.
> **STE:** Do the build.
> **Non-STE:** Perform the build.

*Ref: master.md - Dictionary entry perform (v), Page 20, 146*

---

## PERFORMANCE (n)
- **Original:** How well something operates. THE PERFORMANCE OF THE ENGINE.
- **Code-domain:** How well software runs. THE PERFORMANCE OF THE QUERY.
> **STE:** The performance of the query is good.
> **Non-STE:** The query runs fast.

*Ref: master.md - Dictionary entry PERFORMANCE (n), Page 20*

---

## PERMANENT (adj)
- **Original:** Lasting, not temporary. A PERMANENT MARK.
- **Code-domain:** Not temporary or volatile. PERMANENT STORAGE.
> **STE:** Write the data to permanent storage.
> **Non-STE:** Write the data to persistent storage.

*Ref: master.md - Dictionary entry PERMANENT (adj), Page 20*

---

## PERMIT (v) - UNNAPROVED
- **Original:** LET (v), ALLOW (v). THE RULES LET YOU USE THIS TOOL.
- **Code-domain:** LET (v), ALLOW (v). THE API LETS YOU SEND 100 REQUESTS PER MINUTE.
> **STE:** The API lets you send 100 requests per minute.
> **Non-STE:** The API permits 100 requests per minute.

*Ref: master.md - Dictionary entry permit (v)*

---

## PERSON (n)
- **Original:** A human being. ONLY ONE PERSON CAN DO THIS TASK.
- **Code-domain:** A human being (for user-facing docs). ONLY ONE PERSON CAN ACCESS THE ACCOUNT.
> **STE:** Only one person can access the account.
> **Non-STE:** Only a single user can access the account.

*Ref: master.md - Dictionary entry PERSON (n), Page 20*

---

## PIPE (n) - (TN)
- **Original:** A tube. Code-domain: A data channel.
- **Code-domain:** A data channel or streaming operator. PIPES CONNECT THE COMMANDS.
> **STE:** Use a pipe to connect the commands.
> **Non-STE:** Use the pipe operator to connect the commands.

*Ref: Code-domain technical noun*

---

## PLACE (n), PLACE (v)
- **Original:** A location. THE PLACE OF INSTALLATION. / To put. PLACE THE COMPONENT IN THE RACK.
- **Code-domain:** A location. THE PLACE IN THE CODE. / To insert. PLACE THE HOOK IN THE LIFECYCLE.
> **STE:** Place the hook in the lifecycle at the right position.
> **Non-STE:** Insert the hook into the lifecycle.

*Ref: master.md - Dictionary entry place (n), Page 20*

---

## PLUS (prep)
- **Original:** With the addition of. 3 PLUS 4 IS 7.
- **Code-domain:** Mathematical addition. THE TOTAL IS THE BASE PLUS THE OVERHEAD.
> **STE:** The total is the base plus the overhead.
> **Non-STE:** The total is the sum of the base and overhead.

*Ref: master.md - Dictionary entry PLUS (prep), Page 20*

---

## POINT (n)
- **Original:** A location or stage. THE POINT OF FAILURE.
- **Code-domain:** A location or stage. THE ENTRY POINT OF THE APPLICATION.
> **STE:** The entry point of the application is `main()`.
> **Non-STE:** The application starts at `main()`.

*Ref: master.md - Dictionary entry POINT (n), Page 21*

---

## PORT (n) - (TN)
- **Original:** A harbor. Code-domain: A network endpoint.
- **Code-domain:** A network communication endpoint. THE APPLICATION LISTENS ON PORT 8080.
> **STE:** The application listens on port 8080.
> **Non-STE:** The application uses port 8080.

*Ref: Code-domain technical noun*

---

## POSITION (n)
- **Original:** The location of something. THE POSITION OF THE LEVER.
- **Code-domain:** A location or placement. THE POSITION OF THE ELEMENT IN THE ARRAY.
> **STE:** The position of the element in the array is 0.
> **Non-STE:** The index of the element in the array is 0.

*Ref: master.md - Dictionary entry POSITION (n), Page 21*

---

## POSSIBLE (adj)
- **Original:** That can occur. A POSSIBLE CAUSE.
- **Code-domain:** That can occur. A POSSIBLE SOLUTION.
> **STE:** A possible solution is to increase the timeout.
> **Non-STE:** One solution could be to increase the timeout.

*Ref: master.md - Dictionary entry POSSIBLE (adj), Page 21*

---

## POWER (n)
- **Original:** Energy or electricity. THE ELECTRICAL POWER.
- **Code-domain:** Computing resources. THE PROCESSING POWER OF THE SERVER.
> **STE:** The processing power of the server is sufficient.
> **Non-STE:** The server has enough CPU.

*Ref: master.md - Dictionary entry POWER (n)*

---

## PREPARE (v)
- **Original:** To make ready. PREPARE THE SURFACE.
- **Code-domain:** To make ready. PREPARE THE ENVIRONMENT FOR DEPLOYMENT.
> **STE:** Prepare the environment for deployment.
> **Non-STE:** Set up the environment for deployment.

*Ref: master.md - Dictionary entry PREPARE (v), Page 21*

---

## PREVENT (v)
- **Original:** To stop from occurring. PREVENT ACCIDENTS.
- **Code-domain:** To stop from occurring. PREVENT SQL INJECTION.
> **STE:** Use parameterized queries to prevent SQL injection.
> **Non-STE:** Use parameterized queries to avoid SQL injection.

*Ref: master.md - Dictionary entry PREVENT (v)*

---

## PREVIOUS (adj)
- **Original:** That came before. THE PREVIOUS STEP.
- **Code-domain:** That came before. THE PREVIOUS VERSION.
> **STE:** The previous version had a bug.
> **Non-STE:** The prior version had a bug.

*Ref: master.md - Dictionary entry PREVIOUS (adj), Page 21*

---

## PRIMARY (adj)
- **Original:** Most important. THE PRIMARY CAUSE.
- **Code-domain:** Most important or main. THE PRIMARY KEY OF THE TABLE.
> **STE:** The primary key of the table is the `id` field.
> **Non-STE:** The main key of the table is the `id` field.

*Ref: master.md - Dictionary entry PRIMARY (adj)*

---

## PROBLEM (n)
- **Original:** A difficulty. FIND THE CAUSE OF THE PROBLEM.
- **Code-domain:** A difficulty or defect. IDENTIFY THE ROOT CAUSE OF THE PROBLEM.
> **STE:** Identify the root cause of the problem.
> **Non-STE:** Find what caused the issue.

*Ref: master.md - Dictionary entry PROBLEM (n), Page 22*

---

## PROCEDURE (n)
- **Original:** A set of steps. DO THE PROCEDURE.
- **Code-domain:** A set of steps. DO THE DEPLOYMENT PROCEDURE.
> **STE:** Do the deployment procedure.
> **Non-STE:** Follow the deployment procedure.

*Ref: master.md - Dictionary entry PROCEDURE (n), Page 22*

---

## PROCESS (n), PROCESS (v) - UNNAPROVED
- **Original:** A series of actions. THE INSTALLATION PROCESS. / Not approved as verb; use a specific verb.
- **Code-domain:** A running program. THE PROCESS PID IS 1234. / To handle. PROCESS THE REQUEST. (TV)
> **STE:** Process the request synchronously.
> **Non-STE:** Handle the request synchronously.

> **Note:** PROCESS (v) is a technical verb (TV) in code-domain per Rule 1.12.

*Ref: master.md - Dictionary entry process (n), Page 22*

---

## PROVIDE (v) - UNNAPROVED
- **Original:** GIVE (v), SUPPLY (v). GIVE THE INFORMATION.
- **Code-domain:** GIVE (v), RETURN (v). RETURN THE RESULT.
> **STE:** The function returns the result.
> **Non-STE:** The function provides the result.

*Ref: master.md - Dictionary entry provide (v), Page 22*

---

## PULL (v)
- **Original:** To apply force to move toward. PULL THE LEVER.
- **Code-domain:** To fetch or retrieve. PULL THE LATEST CHANGES FROM THE REPOSITORY.
> **STE:** Pull the latest changes from the repository.
> **Non-STE:** Fetch the latest changes from the repository.

*Ref: master.md - Dictionary entry PULL (v)*

---

## PUSH (v)
- **Original:** To apply force to move away. PUSH THE BUTTON.
- **Code-domain:** To send or upload. PUSH THE COMMIT TO THE REMOTE.
> **STE:** Push the commit to the remote.
> **Non-STE:** Upload the commit to the remote.

*Ref: master.md - Dictionary entry PUSH (v)*

---

## PUT (v)
- **Original:** To place. PUT THE COMPONENT IN THE CONTAINER.
- **Code-domain:** To place or set. PUT THE VALUE IN THE VARIABLE.
> **STE:** Put the value in the variable.
> **Non-STE:** Assign the value to the variable.

*Ref: master.md - Dictionary entry PUT (v), Page 22*

---

# Q

## QUALITY (n)
- **Original:** The standard of something. THE QUALITY OF THE MATERIAL.
- **Code-domain:** The standard of code. CODE QUALITY IS IMPORTANT.
> **STE:** Code quality is important.
> **Non-STE:** The standard of the code is important.

*Ref: master.md - Dictionary entry QUALITY (n), Page 22*

---

## QUANTITY (n)
- **Original:** An amount. A LARGE QUANTITY.
- **Code-domain:** An amount. A QUANTITY OF DATA.
> **STE:** A large quantity of data.
> **Non-STE:** A lot of data.

*Ref: master.md - Dictionary entry QUANTITY (n), Page 22*

---

## QUERY (n) - (TN)
- **Original:** A question. Code-domain: A database request.
- **Code-domain:** A request to a database. THE QUERY RETURNS 10 ROWS.
> **STE:** The query returns 10 rows.
> **Non-STE:** The SQL statement returns 10 rows.

*Ref: Code-domain technical noun*

---

## QUICK (adj), QUICKLY (adv)
- **Original:** At high speed. QUICK MOVEMENT. / MOVE QUICKLY.
- **Code-domain:** Fast. QUICK RESPONSE. / PROCESS THE REQUEST QUICKLY.
> **STE:** Process the request quickly.
> **Non-STE:** Process the request fast.

*Ref: master.md - Dictionary entry QUICKLY (adv)*

---

# R

## RAISE (v)
- **Original:** To lift. RAISE THE COMPONENT.
- **Code-domain:** To throw or increase. RAISE AN EXCEPTION. / RAISE THE LOG LEVEL.
> **STE:** Raise an exception when the value is null.
> **Non-STE:** Throw an exception when the value is null.

*Ref: master.md - Dictionary entry RAISE (v), Page 22*

---

## RANGE (n)
- **Original:** The area between limits. THE TEMPERATURE RANGE.
- **Code-domain:** A span of values. THE PORT RANGE IS 8000-8080.
> **STE:** The port range is 8000-8080.
> **Non-STE:** The ports go from 8000 to 8080.

*Ref: master.md - Dictionary entry RANGE (n)*

---

## READ (v)
- **Original:** To look at and understand. READ THE INSTRUCTIONS.
- **Code-domain:** To access data from storage. READ THE FILE FROM DISK.
> **STE:** Read the file from disk.
> **Non-STE:** Load the file from disk.

*Ref: master.md - Dictionary entry READ (v)*

---

## READY (adj)
- **Original:** Prepared for use. THE UNIT IS READY.
- **Code-domain:** Prepared for use. THE BUILD IS READY FOR DEPLOYMENT.
> **STE:** The build is ready for deployment.
> **Non-STE:** The build can be deployed.

*Ref: master.md - Dictionary entry READY (adj)*

---

## RECEIVE (v)
- **Original:** To get. RECEIVE THE DATA.
- **Code-domain:** To accept incoming data. RECEIVE THE HTTP RESPONSE.
> **STE:** Receive the HTTP response.
> **Non-STE:** Get the HTTP response.

*Ref: master.md - Dictionary entry RECEIVE (v)*

---

## RECOMMEND (v)
- **Original:** To suggest as good. THE MANUFACTURER RECOMMENDS THIS PROCEDURE.
- **Code-domain:** To suggest. THE STYLE GUIDE RECOMMENDS THIS FORMAT.
> **STE:** The style guide recommends this format.
> **Non-STE:** The style guide suggests this format.

*Ref: master.md - Dictionary entry RECOMMEND (v), Page 23*

---

## RECORD (v)
- **Original:** To write down. RECORD THE VALUE.
- **Code-domain:** To log or persist. RECORD THE ERROR IN THE LOG.
> **STE:** Record the error in the log.
> **Non-STE:** Log the error.

*Ref: master.md - Dictionary entry RECORD (v), Page 10*

---

## REDUCE (v) - UNNAPROVED
- **Original:** DECREASE (v). DECREASE THE PRESSURE.
- **Code-domain:** DECREASE (v). DECREASE THE MEMORY USAGE.
> **STE:** Decrease the memory usage.
> **Non-STE:** Reduce the memory usage.

*Ref: master.md - Dictionary entry reduce (v), Page 23*

---

## REFER (v)
- **Original:** To direct attention to. REFER TO THE MANUAL.
- **Code-domain:** To reference. REFER TO THE API DOCUMENTATION.
> **STE:** Refer to the API documentation for details.
> **Non-STE:** See the API documentation for details.

*Ref: master.md - Dictionary entry REFER (v), Page 23*

---

## REFRESH (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To reload or update. REFRESH THE PAGE TO SEE THE CHANGES.
> **STE:** Refresh the page to see the changes.
> **Non-STE:** Reload the page to see the changes.

*Ref: Code-domain technical verb*

---

## REJECT (v)
- **Original:** To refuse to accept. REJECT THE COMPONENT.
- **Code-domain:** To refuse a request or input. REJECT THE COMMIT IF TESTS FAIL.
> **STE:** Reject the commit if tests fail.
> **Non-STE:** Deny the commit if tests fail.

*Ref: master.md - Dictionary entry REJECT (v)*

---

## RELEASE (v)
- **Original:** To let go. RELEASE THE LATCH.
- **Code-domain:** To publish or free. RELEASE THE NEW VERSION. / RELEASE THE MEMORY.
> **STE:** Release the new version to production.
> **Non-STE:** Publish the new version to production.

> **STE:** Release the memory after use.
> **Non-STE:** Free the memory after use.

*Ref: master.md - Dictionary entry RELEASE (v)*

---

## REMAINING (adj)
- **Original:** Left over. THE REMAINING TIME.
- **Code-domain:** Left over. THE REMAINING WARNINGS.
> **STE:** Fix the remaining warnings.
> **Non-STE:** Fix the leftover warnings.

*Ref: master.md - Dictionary entry REMAINING (adj), Page 23*

---

## REMOVE (v)
- **Original:** To take away. REMOVE THE OLD FILTER.
- **Code-domain:** To delete or uninstall. REMOVE THE DEPRECATED FUNCTION.
> **STE:** Remove the deprecated function.
> **Non-STE:** Delete the deprecated function.

*Ref: master.md - Dictionary entry REMOVE (v)*

---

## REPAIR (v)
- **Original:** To fix. REPAIR THE DAMAGED PART.
- **Code-domain:** To fix. REPAIR THE BROKEN BUILD.
> **STE:** Repair the broken build.
> **Non-STE:** Fix the broken build.

*Ref: master.md - Dictionary entry REPAIR (v), Page 23*

---

## REPEAT (v)
- **Original:** To do again. REPEAT THE TEST.
- **Code-domain:** To loop or do again. REPEAT THE OPERATION FOR EACH ITEM.
> **STE:** Repeat the operation for each item.
> **Non-STE:** Loop through the items and do the operation.

*Ref: master.md - Dictionary entry REPEAT (v)*

---

## REPLACE (v)
- **Original:** To put a new thing in place of the old. REPLACE THE FILTER.
- **Code-domain:** To substitute. REPLACE THE OLD LIBRARY WITH THE NEW ONE.
> **STE:** Replace the old library with the new one.
> **Non-STE:** Swap the old library for the new one.

*Ref: master.md - Dictionary entry REPLACE (v)*

---

## REPORT (n), REPORT (v) - (TN/TV)
- **Original:** An account. GENERATE A REPORT. / To tell. REPORT THE ERROR.
- **Code-domain:** A summary. GENERATE A COVERAGE REPORT. / To notify. REPORT THE BUG.
> **STE:** Report the bug in the issue tracker.
> **Non-STE:** Log the bug in the issue tracker.

*Ref: Code-domain technical noun/verb*

---

## REQUEST (n), REQUEST (v) - (TN/TV)
- **Original:** An act of asking. Code-domain: An HTTP or programmatic request.
- **Code-domain:** A call to a service. THE HTTP REQUEST RETURNS 200 OK.
> **STE:** The HTTP request returns 200 OK.
> **Non-STE:** The HTTP call returns 200 OK.

*Ref: Code-domain technical noun*

---

## REQUIRE (v) - UNNAPROVED
- **Original:** MUST (v), NECESSARY (adj). YOU MUST USE THE CORRECT TOOL.
- **Code-domain:** MUST (v). YOU MUST INSTALL NODE.JS.
> **STE:** You must install Node.js.
> **Non-STE:** The project requires Node.js.

*Ref: master.md - Dictionary entry require (v), Page 23*

---

## RESOURCE (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A system asset (memory, CPU, file handle). FREE THE RESOURCES AFTER USE.
> **STE:** Free the resources after use.
> **Non-STE:** Release the resources after use.

*Ref: Code-domain technical noun*

---

## RESPONSE (n) - (TN)
- **Original:** An answer. Code-domain: An HTTP or API response.
- **Code-domain:** Data returned by a service. THE RESPONSE CONTAINS THE USER DATA.
> **STE:** The response contains the user data.
> **Non-STE:** The reply contains the user data.

*Ref: Code-domain technical noun*

---

## RESTART (v)
- **Original:** To start again. RESTART THE ENGINE.
- **Code-domain:** To start again. RESTART THE SERVICE.
> **STE:** Restart the service.
> **Non-STE:** Stop and start the service.

*Ref: master.md - Dictionary entry RESTART (v)*

---

## RESULT (n)
- **Original:** The outcome. THE RESULT OF THE TEST.
- **Code-domain:** The output. THE RESULT OF THE QUERY.
> **STE:** The result of the query is an empty set.
> **Non-STE:** The query returns no rows.

*Ref: master.md - Dictionary entry RESULT (n)*

---

## RETRY (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To attempt again. RETRY THE REQUEST AFTER 5 SECONDS.
> **STE:** Retry the request after 5 seconds.
> **Non-STE:** Try the request again after 5 seconds.

*Ref: Code-domain technical verb*

---

## RETURN (v)
- **Original:** To go or give back. RETURN THE TOOL TO THE STORE.
- **Code-domain:** To send a value back from a function. RETURN THE RESULT.
> **STE:** The function returns the computed value.
> **Non-STE:** The function gives back the computed value.

*Ref: master.md - Dictionary entry RETURN (v)*

---

## REVIEW (n) - UNNAPROVED
- **Original:** EXAMINE (v). EXAMINE THE DOCUMENT AGAIN.
- **Code-domain:** EXAMINE (v). EXAMINE THE CODE FOR ISSUES.
> **STE:** Examine the code for issues.
> **Non-STE:** Review the code for issues.

> **Note:** REVIEW is a technical noun (TN) in code-domain (code review) per Rule 1.5.

*Ref: master.md - Dictionary entry review (n), Page 23*

---

## RIGHT (adj), RIGHT (adv)
- **Original:** Correct. THE RIGHT VALUE. / In a direction opposite to left. MOVE THE LEVER RIGHT.
- **Code-domain:** Correct. THE RIGHT SOLUTION. / Right-side. ALIGN THE TEXT RIGHT.
> **STE:** Align the text right.
> **Non-STE:** Align the text to the right.

*Ref: master.md - Dictionary entry RIGHT (adj)*

---

## RISK (n)
- **Original:** The possibility of a bad result. THE RISK OF FIRE.
- **Code-domain:** The possibility of a bad result. THE RISK OF DATA LOSS.
> **STE:** The risk of data loss is small.
> **Non-STE:** There is little chance of data loss.

*Ref: master.md - Dictionary entry RISK (n)*

---

## ROOT (n) - (TN)
- **Original:** The part of a plant underground. Code-domain: The base of a hierarchy.
- **Code-domain:** The base directory or top-level access. THE ROOT OF THE PROJECT.
> **STE:** The config file is in the root of the project.
> **Non-STE:** The config file is at the top level of the project.

> **STE:** Run the command as root.
> **Non-STE:** Run the command with superuser privileges.

*Ref: Code-domain technical noun*

---

## ROUTE (n) - (TN)
- **Original:** A way. Code-domain: A URL pattern in a web framework.
- **Code-domain:** A URL endpoint mapping. THE ROUTE `/users` RETURNS THE USER LIST.
> **STE:** The route `/users` returns the user list.
> **Non-STE:** The endpoint `/users` returns the user list.

*Ref: Code-domain technical noun*

---

## RULE (n)
- **Original:** A regulation. THE RULES OF THE STANDARD.
- **Code-domain:** A regulation or validation condition. THE VALIDATION RULE CHECKS THE EMAIL FORMAT.
> **STE:** The validation rule checks the email format.
> **Non-STE:** The validation checks the email format.

*Ref: master.md - Dictionary entry RULE (n)*

---

## RUN (v)
- **Original:** To operate or move fast. RUN THE ENGINE.
- **Code-domain:** To execute. RUN THE SCRIPT FROM THE TERMINAL.
> **STE:** Run the script from the terminal.
> **Non-STE:** Execute the script from the terminal.

*Ref: master.md - Dictionary entry RUN (v)*

---

# S

## SAFE (adj), SAFETY (n)
- **Original:** Not dangerous. A SAFE PROCEDURE. / Freedom from danger. FOR YOUR SAFETY, WEAR GOGGLES.
- **Code-domain:** Secure, not risky. A SAFE DEFAULT. / Security. FOR DATA SAFETY, ENCRYPT THE BACKUP.
> **STE:** A safe default value prevents crashes.
> **Non-STE:** A sensible default value prevents crashes.

> **STE:** For data safety, encrypt the backup.
> **Non-STE:** For security, encrypt the backup.

*Ref: master.md - Dictionary entry SAFE (adj), Page 23*

---

## SAME (adj)
- **Original:** Not different. THE SAME TYPE.
- **Code-domain:** Not different. THE SAME RESULT.
> **STE:** The two functions return the same result.
> **Non-STE:** The two functions return identical results.

*Ref: master.md - Dictionary entry SAME (adj)*

---

## SAMPLE (n)
- **Original:** A small part that shows the quality. A SAMPLE OF THE MATERIAL.
- **Code-domain:** An example or specimen. A CODE SAMPLE.
> **STE:** A code sample is in the `examples/` directory.
> **Non-STE:** An example is in the `examples/` directory.

*Ref: master.md - Dictionary entry SAMPLE (n), Page 23*

---

## SAVE (v)
- **Original:** To keep for later use. SAVE THE DATA.
- **Code-domain:** To persist data. SAVE THE FILE TO DISK.
> **STE:** Save the file to disk.
> **Non-STE:** Write the file to disk.

*Ref: master.md - Dictionary entry SAVE (v)*

---

## SCHEDULE (v)
- **Original:** To plan at a time. SCHEDULE THE MAINTENANCE.
- **Code-domain:** To plan execution. SCHEDULE THE JOB TO RUN DAILY.
> **STE:** Schedule the job to run daily.
> **Non-STE:** Set the job to run daily.

*Ref: master.md - Dictionary entry SCHEDULE (v)*

---

## SEARCH (v) - (TV)
- **Original:** To look for. SEARCH THE AREA.
- **Code-domain:** To look for data. SEARCH THE LOGS FOR ERROR MESSAGES.
> **STE:** Search the logs for error messages.
> **Non-STE:** Look through the logs for error messages.

*Ref: Code-domain technical verb*

---

## SECTION (n)
- **Original:** A part. A SECTION OF THE MANUAL.
- **Code-domain:** A part of a document or code. REFER TO THE SECURITY SECTION.
> **STE:** Refer to the Security section of the README.
> **Non-STE:** See the Security part of the README.

*Ref: master.md - Dictionary entry SECTION (n)*

---

## SEE (v)
- **Original:** To perceive with eyes. SEE THE INDICATOR.
- **Code-domain:** To reference. SEE THE DOCUMENTATION.
> **STE:** See the documentation for details.
> **Non-STE:** Refer to the documentation for details.

*Ref: master.md - Dictionary entry SEE (v), Page 24*

---

## SELECT (v)
- **Original:** To choose. SELECT THE CORRECT TOOL.
- **Code-domain:** To choose or query. SELECT THE DATABASE FROM THE LIST. / SELECT RECORDS FROM THE TABLE.
> **STE:** Select the database from the list.
> **Non-STE:** Choose the database from the list.

> **Note:** SELECT is a technical verb (TV) in SQL per Rule 1.12.

*Ref: master.md - Dictionary entry SELECT (v), Page 24*

---

## SEND (v)
- **Original:** To cause to go. SEND THE DATA.
- **Code-domain:** To transmit. SEND THE REQUEST TO THE SERVER.
> **STE:** Send the request to the server.
> **Non-STE:** Make the request to the server.

*Ref: master.md - Dictionary entry SEND (v)*

---

## SEPARATE (adj) - UNNAPROVED
- **Original:** ISOLATED (adj), DIFFERENT (adj), NOT CONNECTED, NOT ATTACHED.
- **Code-domain:** ISOLATED (adj), DIFFERENT (adj), NOT CONNECTED. KEEP THE MODULES ISOLATED.
> **STE:** Keep the modules isolated from each other.
> **Non-STE:** Keep the modules separate from each other.

*Ref: master.md - Dictionary entry separate (adj), Page 24, 373*

---

## SEQUENCE (n)
- **Original:** The relation of items that follow one after the other. TIGHTEN THE BOLTS IN THE SEQUENCE THAT IS GIVEN IN FIGURE 3.
- **Code-domain:** An ordered series. EXECUTE THE STEPS IN THE GIVEN SEQUENCE.
> **STE:** Execute the steps in the given sequence.
> **Non-STE:** Execute the steps in order.

*Ref: master.md - Dictionary entry SEQUENCE (n), Page 373*

---

## SERVER (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A computer that provides services. THE SERVER LISTENS ON PORT 443.
> **STE:** The server listens on port 443.
> **Non-STE:** The service listens on port 443.

*Ref: Code-domain technical noun*

---

## SERVICE (n) - (TN)
- **Original:** A utility. Code-domain: A background process or API.
- **Code-domain:** A running application. THE AUTHENTICATION SERVICE IS DOWN.
> **STE:** The authentication service is down.
> **Non-STE:** The auth service is not running.

*Ref: Code-domain technical noun*

---

## SET (n), SET (v)
- **Original:** A group of items. A SET OF TOOLS. / To put into a condition. SET THE SWITCH TO ON.
- **Code-domain:** A collection. A SET OF CONFIG VALUES. / To assign. SET THE VARIABLE TO 10.
> **STE:** Set the variable to 10.
> **Non-STE:** Assign 10 to the variable.

*Ref: master.md - Dictionary entry SET (v), Page 374*

---

## SHORT (adj)
- **Original:** Having small length or duration. A SHORT CABLE. / A SHORT TIME.
- **Code-domain:** Having small length or duration. A SHORT DESCRIPTION. / A SHORT TIMEOUT.
> **STE:** A short timeout of 1 second.
> **Non-STE:** A brief timeout of 1 second.

*Ref: master.md - Dictionary entry SHORT (adj), Page 24, 376*

---

## SHOW (v)
- **Original:** To cause to be seen. THE INDICATOR SHOWS THE VALUE.
- **Code-domain:** To display. THE COMMAND SHOWS THE FILE CONTENTS.
> **STE:** The command shows the file contents.
> **Non-STE:** The command displays the file contents.

*Ref: master.md - Dictionary entry SHOW (v), Page 24, 377*

---

## SHUT DOWN (v) - UNNAPROVED
- **Original:** STOP (v). STOP THE ENGINE.
- **Code-domain:** STOP (v). STOP THE SERVER.
> **STE:** Stop the server.
> **Non-STE:** Shut down the server.

*Ref: master.md - Dictionary entry shut down (v), Page 377*

---

## SIGNAL (n) - (TN)
- **Original:** A sign. Code-domain: An operating system notification.
- **Code-domain:** An OS-level notification. SEND A SIGTERM SIGNAL TO THE PROCESS.
> **STE:** Send a SIGTERM signal to the process.
> **Non-STE:** Terminate the process.

*Ref: Code-domain technical noun*

---

## SIMPLE (adj)
- **Original:** Not complex. A SIMPLE PROCEDURE.
- **Code-domain:** Not complex. A SIMPLE FUNCTION.
> **STE:** A simple function with one responsibility.
> **Non-STE:** A straightforward function with one responsibility.

*Ref: master.md - Dictionary entry SIMPLE (adj)*

---

## SINGLE (adj)
- **Original:** One only. A SINGLE COMPONENT.
- **Code-domain:** One only. A SINGLE INSTANCE.
> **STE:** A single instance of the application.
> **Non-STE:** One instance of the application.

*Ref: master.md - Dictionary entry SINGLE (adj), Page 24*

---

## SIZE (n)
- **Original:** How large something is. THE SIZE OF THE CONTAINER.
- **Code-domain:** How large something is. THE SIZE OF THE FILE.
> **STE:** The size of the file is 2 MB.
> **Non-STE:** The file is 2 MB.

*Ref: master.md - Dictionary entry SIZE (n), Page 24*

---

## SLOW (adj), SLOWLY (adv)
- **Original:** At low speed. SLOW MOVEMENT. / In a slow manner. TURN THE KNOB SLOWLY.
- **Code-domain:** At low speed. SLOW RESPONSE. / Gradually. INCREASE THE VALUE SLOWLY.
> **STE:** Slowly increase the timeout value.
> **Non-STE:** Gradually increase the timeout value.

*Ref: master.md - Dictionary entry SLOW (adj), Page 380*

---

## SMALL (adj)
- **Original:** Less than average in dimension, quantity, quality, or capacity. IF THE TEMPERATURE INCREASES SUDDENLY, ADD A SMALL QUANTITY OF REAGENT.
- **Code-domain:** Less than average. A SMALL AMOUNT OF MEMORY.
> **STE:** A small amount of memory is allocated.
> **Non-STE:** A negligible amount of memory is allocated.

*Ref: master.md - Dictionary entry SMALL (adj), Page 24, 381*

---

## SOCKET (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A network communication endpoint. OPEN A SOCKET ON PORT 3000.
> **STE:** Open a socket on port 3000.
> **Non-STE:** Create a connection on port 3000.

*Ref: Code-domain technical noun*

---

## SOLUTION (n)
- **Original:** 1. A liquid with dissolved material. PREPARE THE SOLUTION. 2. The answer to a problem. THE TEAM'S WORK WAS IMPORTANT FOR THE SOLUTION OF THE TECHNICAL PROBLEM.
- **Code-domain:** 1. Not applicable. 2. A resolution. THE SOLUTION TO THE MEMORY LEAK IS TO USE WEAK REFERENCES.
> **STE:** The solution to the memory leak is to use weak references.
> **Non-STE:** Fix the memory leak by using weak references.

*Ref: master.md - Dictionary entry SOLUTION (n), Page 24, 383*

---

## SOME (adj), SOME (pron)
- **Original:** Related to a quantity not specified. SOME MODELS DO NOT HAVE THIS FUNCTION.
- **Code-domain:** An unspecified number. SOME TESTS FAIL UNDER LOAD.
> **STE:** Some tests fail under load.
> **Non-STE:** A few tests fail under load.

*Ref: master.md - Dictionary entry SOME (adj), Page 383*

---

## SOURCE (n)
- **Original:** 1. Something that supplies energy or data. THE SOLAR PANEL IS A SATISFACTORY SOURCE OF ENERGY. 2. The point where something starts. FIND THE SOURCE OF THE LEAKAGE.
- **Code-domain:** 1. Origin of data. THE DATABASE IS THE SOURCE OF TRUTH. 2. Point of origin. FIND THE SOURCE OF THE BUG.
> **STE:** Find the source of the bug.
> **Non-STE:** Locate where the bug originates.

*Ref: master.md - Dictionary entry SOURCE (n), Page 24, 384*

---

## SPACE (n)
- **Original:** A distance, area, or volume. PUT THE SEALANT INTO THE SPACE BEHIND THE FLANGE.
- **Code-domain:** Disk or memory capacity. MAKE SURE THAT THERE IS SUFFICIENT DISK SPACE.
> **STE:** Make sure that there is sufficient disk space.
> **Non-STE:** Check that there is enough disk space.

*Ref: master.md - Dictionary entry SPACE (n), Page 384*

---

## SPECIAL (adj), SPECIALLY (adv)
- **Original:** For a specified function. TIGHTEN THE SPECIAL NUT. / In a special manner. THIS EXTRACTOR IS SPECIALLY MADE.
- **Code-domain:** Purpose-specific. USE THE SPECIAL CONFIG FOR STAGING.
> **STE:** Use the special config for staging.
> **Non-STE:** Use the staging-specific config.

*Ref: master.md - Dictionary entry SPECIAL (adj), Page 384*

---

## SPECIFIED (adj)
- **Original:** Given in, identified in, or related to a specification. INFLATE THE TIRE WITH NITROGEN TO THE SPECIFIED PRESSURE.
- **Code-domain:** Given in a specification or document. USE THE SPECIFIED PORT NUMBER.
> **STE:** Use the specified port number from the config.
> **Non-STE:** Use the port number that is given in the config.

*Ref: master.md - Dictionary entry SPECIFIED (adj), Page 385*

---

## SPEED (n)
- **Original:** The rate of movement. THE MAXIMUM PERMITTED SPEED IS 30 MPH.
- **Code-domain:** The rate of processing. THE SPEED OF THE QUERY IS FAST.
> **STE:** The speed of the query is fast.
> **Non-STE:** The query is fast.

*Ref: master.md - Dictionary entry SPEED (n), Page 25*

---

## STACK (n) - (TN)
- **Original:** A pile. Code-domain: A LIFO data structure or technology stack.
- **Code-domain:** A LIFO data structure. PUSH THE VALUE ONTO THE STACK.
> **STE:** Push the value onto the stack.
> **Non-STE:** Add the value to the stack.

*Ref: Code-domain technical noun*

---

## STAGE (n) - UNNAPROVED
- **Original:** STEP (n). DURING THIS STEP, DO NOT REMOVE THE PIN.
- **Code-domain:** STEP (n). DURING THIS STEP, DO NOT MERGE THE BRANCH.
> **STE:** During this step, do not merge the branch.
> **Non-STE:** At this stage, do not merge the branch.

> **Note:** STAGE is a technical verb (TV) in version control (git stage) per Rule 1.12.

*Ref: master.md - Dictionary entry stage (n), Page 25*

---

## STANDARD (adj)
- **Original:** Related to equipment and procedures that are normally used. IN THIS PROCEDURE, USE STANDARD TOOLS.
- **Code-domain:** Conforming to norms. FOLLOW THE STANDARD CODING CONVENTIONS.
> **STE:** Follow the standard coding conventions.
> **Non-STE:** Follow the usual coding conventions.

*Ref: master.md - Dictionary entry STANDARD (adj), Page 388*

---

## START (n), START (v)
- **Original:** The beginning. MOVEMENT CAN BE SLOW AT THE START. / To begin. START THE ENGINE.
- **Code-domain:** To begin. START THE APPLICATION.
> **STE:** Start the application.
> **Non-STE:** Launch the application.

*Ref: master.md - Dictionary entry START (v), Page 388*

---

## STATE (n) - UNNAPROVED
- **Original:** CONDITION (n). EXAMINE THE CONDITION OF THE UNIT.
- **Code-domain:** CONDITION (n). EXAMINE THE CONDITION OF THE SYSTEM.
> **STE:** Examine the condition of the system.
> **Non-STE:** Examine the state of the system.

> **Note:** STATE is a technical noun (TN) in programming (state machine, application state) per Rule 1.5.

*Ref: master.md - Dictionary entry state (n), Page 388*

---

## STATUS (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** The current condition. THE STATUS OF THE SERVICE IS "HEALTHY."
> **STE:** The status of the service is "healthy."
> **Non-STE:** The service is healthy.

*Ref: Code-domain technical noun*

---

## STAY (v)
- **Original:** To continue to be in a location or condition. MAKE SURE THAT THE ASSEMBLED PARTS STAY ALIGNED. No other verb forms.
- **Code-domain:** To remain. MAKE SURE THAT THE CONNECTION STAYS OPEN.
> **STE:** Make sure that the connection stays open.
> **Non-STE:** Keep the connection open.

*Ref: master.md - Dictionary entry STAY (v), Page 25, 389*

---

## STEP (n)
- **Original:** A specified part of a procedure. DO STEPS 13 THRU 16 A MINIMUM OF THREE TIMES.
- **Code-domain:** A specified part of a procedure. DO STEPS 1 THRU 5 IN THE GIVEN ORDER.
> **STE:** Do steps 1 through 5 in the given order.
> **Non-STE:** Follow the procedure steps 1-5.

*Ref: master.md - Dictionary entry STEP (n), Page 389*

---

## STOP (v)
- **Original:** 1. To cause the end of a procedure, movement, or operation. STOP THE ENGINE. 2. To come to an end. WHEN THE FLOW STOPS, REMOVE THE DRAIN HOSE.
- **Code-domain:** 1. To terminate. STOP THE PROCESS. 2. To halt. WHEN THE ERRORS STOP, CHECK THE LOGS.
> **STE:** Stop the process.
> **Non-STE:** Kill the process.

> **STE:** When the errors stop, check the logs.
> **Non-STE:** When the errors cease, check the logs.

*Ref: master.md - Dictionary entry STOP (v), Page 390*

---

## STORE (v) - UNNAPROVED
- **Original:** KEEP (v), CONTAIN (v). KEEP THE CARTRIDGES IN A SAFETY AREA.
- **Code-domain:** KEEP (v), SAVE (v). KEEP THE CONFIG FILES IN VERSION CONTROL.
> **STE:** Keep the config files in version control.
> **Non-STE:** Store the config files in version control.

> **Note:** STORE is a technical verb (TV) in programming (data store) per Rule 1.12.

*Ref: master.md - Dictionary entry store (v), Page 25*

---

## STREAM (n) - (TN)
- **Original:** A flow of liquid. Code-domain: A sequence of data.
- **Code-domain:** A continuous flow of data. PROCESS THE DATA AS A STREAM.
> **STE:** Process the data as a stream.
> **Non-STE:** Process the data in chunks.

*Ref: Code-domain technical noun*

---

## STRING (n) - (TN)
- **Original:** A cord. Code-domain: A sequence of characters.
- **Code-domain:** A sequence of characters. THE RESPONSE RETURNS A JSON STRING.
> **STE:** The response returns a JSON string.
> **Non-STE:** The response returns JSON text.

*Ref: Code-domain technical noun*

---

## STRONG (adj)
- **Original:** With much strength, power, or concentration. WHEN WINDS ARE STRONG, MOOR THE AIRCRAFT CAREFULLY.
- **Code-domain:** Robust, high-entropy. USE A STRONG PASSWORD.
> **STE:** Use a strong password.
> **Non-STE:** Use a secure password.

*Ref: master.md - Dictionary entry STRONG (adj), Page 25, 392*

---

## STRUCTURE (n)
- **Original:** 1. A construction. ATTACH THE WIRES TO THE STRUCTURE. 2. The arrangement of something. THE INTRODUCTION GIVES YOU THE STRUCTURE OF THE MAINTENANCE MANUAL.
- **Code-domain:** 1. A data organization. DEFINE THE DATA STRUCTURE. 2. The arrangement. THE STRUCTURE OF THE PROJECT FOLLOWS MVC.
> **STE:** The structure of the project follows MVC.
> **Non-STE:** The project layout follows MVC.

*Ref: master.md - Dictionary entry STRUCTURE (n), Page 392*

---

## SUFFICIENT (adj), SUFFICIENTLY (adv)
- **Original:** Not less (or more) than necessary. ADJUST THE CLAMP UNTIL THERE IS SUFFICIENT FRICTION. / WHEN THE PAINT IS SUFFICIENTLY SOFT, REMOVE IT.
- **Code-domain:** Enough. MAKE SURE THAT THERE IS SUFFICIENT DISK SPACE. / WHEN THE BUILD IS SUFFICIENTLY STABLE, DEPLOY IT.
> **STE:** Make sure that there is sufficient disk space.
> **Non-STE:** Make sure that there is enough disk space.

*Ref: master.md - Dictionary entry SUFFICIENT (adj), Page 394*

---

## SUDDEN (adj), SUDDENLY (adv)
- **Original:** That occurs in a short time. SUDDEN MOVEMENT CAN CAUSE DAMAGE. / In a sudden manner. IF THE TEMPERATURE INCREASES SUDDENLY, STOP THE ENGINE.
- **Code-domain:** Occurring unexpectedly. A SUDDEN SPIKE IN CPU USAGE. / IF THE SERVICE FAILS SUDDENLY, READ THE LOGS.
> **STE:** If the service fails suddenly, read the logs.
> **Non-STE:** If the service fails unexpectedly, read the logs.

*Ref: master.md - Dictionary entry SUDDEN (adj), Page 394*

---

## SUPPLY (n), SUPPLY (v)
- **Original:** Something that is supplied. STOP THE ELECTRICAL POWER SUPPLY. / To give. SUPPLY ELECTRICAL POWER TO THE AUXILIARY SYSTEM.
- **Code-domain:** To provide. SUPPLY THE API KEY AS A QUERY PARAMETER.
> **STE:** Supply the API key as a query parameter.
> **Non-STE:** Provide the API key as a query parameter.

*Ref: master.md - Dictionary entry SUPPLY (v), Page 395*

---

## SURFACE (n)
- **Original:** One or more of the faces of something. CLEAN THE SURFACE WITH A SOFT, DRY CLOTH.
- **Code-domain:** The external layer. THE API SURFACE OF THE LIBRARY IS SMALL.
> **STE:** The API surface of the library is small.
> **Non-STE:** The public interface of the library is small.

*Ref: master.md - Dictionary entry SURFACE (n), Page 26*

---

## SYSTEM (n)
- **Original:** A set of connected things. THE HYDRAULIC SYSTEM.
- **Code-domain:** A set of connected software components. THE AUTHENTICATION SYSTEM USES JWT.
> **STE:** The authentication system uses JWT.
> **Non-STE:** The authentication module uses JWT.

*Ref: master.md - Dictionary entry SYSTEM (n)*

---

# T

## TABLE (n)
- **Original:** A flat surface. Code-domain: A database structure.
- **Code-domain:** A database structure or HTML element. THE USERS TABLE HAS FOUR COLUMNS.
> **STE:** The `users` table has four columns.
> **Non-STE:** The `users` database table has four columns.

*Ref: Code-domain technical noun*

---

## TAG (n) - (TN)
- **Original:** A label. Code-domain: A version control or HTML marker.
- **Code-domain:** A marker. ADD A VERSION TAG TO THE COMMIT.
> **STE:** Add a version tag to the commit.
> **Non-STE:** Mark the commit with a version number.

*Ref: Code-domain technical noun*

---

## TAKE (v) - UNNAPROVED
- **Original:** Use more accurate verbs: REMOVE (v), GET (v), DO (v).
- **Code-domain:** Use more accurate verbs: FETCH (v), CONSUME (v), REQUIRE (v).
> **STE:** The query consumes 100 ms.
> **Non-STE:** The query takes 100 ms.

*Ref: master.md - Dictionary entry take (v), Page 26*

---

## TASK (n)
- **Original:** A piece of work. DO THIS TASK OUTDOORS.
- **Code-domain:** A unit of work. THE ASYNCHRONOUS TASK RUNS IN THE BACKGROUND.
> **STE:** The asynchronous task runs in the background.
> **Non-STE:** The background job runs asynchronously.

*Ref: master.md - Dictionary entry TASK (n), Page 26*

---

## TELL (v)
- **Original:** To give information. TELL THE RAMP AGENT THAT THE BRAKES ARE SET.
- **Code-domain:** To inform. THE LOG FILE TELLS YOU THE ERROR LOCATION.
> **STE:** The log file tells you the error location.
> **Non-STE:** The log file shows you the error location.

*Ref: master.md - Dictionary entry TELL (v), Page 26*

---

## TEMPORARY (adj)
- **Original:** Not permanent. A TEMPORARY SOLUTION.
- **Code-domain:** Not permanent. A TEMPORARY FILE.
> **STE:** Create a temporary file for the intermediate data.
> **Non-STE:** Create a temp file for the intermediate data.

*Ref: master.md - Dictionary entry TEMPORARY (adj)*

---

## TERMINATE (v) - (TV)
- **Original:** To end. Code-domain technical verb.
- **Code-domain:** To forcefully stop. TERMINATE THE HUNG PROCESS.
> **STE:** Terminate the hung process.
> **Non-STE:** Kill the hung process.

*Ref: Code-domain technical verb*

---

## TEST (n)
- **Original:** An examination. DO THE TEST.
- **Code-domain:** An automated verification. RUN THE UNIT TESTS.
> **STE:** Run the unit tests before you merge.
> **Non-STE:** Execute the test suite before merging.

*Ref: master.md - Dictionary entry TEST (n), Page 26*

---

## TEST (v) - UNNAPROVED
- **Original:** Not approved as verb; use TEST (n) with DO. DO A TEST OF THE SYSTEM.
- **Code-domain:** TEST (n) with DO. DO A TEST OF THE MODULE.
> **STE:** Do a test of the module.
> **Non-STE:** Test the module.

> **Note:** TEST (v) is a technical verb (TV) in software development per Rule 1.12.

*Ref: master.md - Dictionary entry test (v), Page 26, 146*

---

## TEXT (n) - (TN)
- **Original:** Written words. Code-domain technical noun.
- **Code-domain:** String data. THE RESPONSE BODY CONTAINS PLAIN TEXT.
> **STE:** The response body contains plain text.
> **Non-STE:** The response body is a string.

*Ref: Code-domain technical noun*

---

## THAN (conj)
- **Original:** Used to compare. MORE THAN THE LIMIT.
- **Code-domain:** Used to compare. FASTER THAN THE PREVIOUS VERSION.
> **STE:** The new version is faster than the previous version.
> **Non-STE:** The new version outperforms the previous version.

*Ref: master.md - Dictionary entry THAN (conj)*

---

## THAT (conj), THAT (pron)
- **Original:** Function word. MAKE SURE THAT THE VALVE IS CLOSED. / The thing specified. USE THE TOOL THAT IS IN THE KIT.
- **Code-domain:** Function word. MAKE SURE THAT THE TESTS PASS. / USE THE CONFIG THAT IS IN THE DEFAULT PROFILE.
> **STE:** Make sure that the tests pass.
> **Non-STE:** Ensure the tests pass.

*Ref: master.md - Dictionary entry THAT (conj), Page 26*

---

## THE (art)
- **Original:** Definite article. THE COMPONENT.
- **Code-domain:** Definite article. THE FUNCTION.
> **STE:** The function returns a value.
> **Non-STE:** Function returns a value.

*Ref: master.md - Dictionary entry THE (art)*

---

## THEN (adv)
- **Original:** At that time or after that. DO THE FIRST STEP. THEN, DO THE SECOND STEP.
- **Code-domain:** After that. COMPILE THE CODE. THEN, RUN THE TESTS.
> **STE:** Compile the code. Then, run the tests.
> **Non-STE:** Compile the code and subsequently run the tests.

*Ref: master.md - Dictionary entry THEN (adv), Page 26*

---

## THICK (adj)
- **Original:** Having large depth or thickness. THICK MATERIAL.
- **Code-domain:** Not commonly applicable. Retained for hardware context.
> **Note:** Domain-specific; limited code-documentation equivalent.

*Ref: master.md - Dictionary entry THICK (adj), Page 26*

---

## THREAD (n) - (TN)
- **Original:** A thin string. Code-domain: An execution context.
- **Code-domain:** A unit of CPU execution. RUN THE TASK IN A SEPARATE THREAD.
> **STE:** Run the task in a separate thread.
> **Non-STE:** Run the task in parallel.

*Ref: Code-domain technical noun*

---

## THROUGH (prep)
- **Original:** From one side to the other. PUSH THE WIRE THROUGH THE HOLE.
- **Code-domain:** Passing via or by means of. ROUTE THE REQUEST THROUGH THE PROXY.
> **STE:** Route the request through the proxy.
> **Non-STE:** Pass the request via the proxy.

*Ref: master.md - Dictionary entry THROUGH (prep)*

---

## THROW (v) - (TV)
- **Original:** To send through air. Code-domain: To raise an exception.
- **Code-domain:** To raise an exception. THE FUNCTION THROWS AN ERROR ON INVALID INPUT.
> **STE:** The function throws an error on invalid input.
> **Non-STE:** The function raises an error on invalid input.

*Ref: Code-domain technical verb*

---

## THUS (adv)
- **Original:** As a result. THUS, THE SYSTEM STOPS.
- **Code-domain:** Therefore. THUS, THE REQUEST FAILS.
> **STE:** The token expires. Thus, the request fails.
> **Non-STE:** The token expires; therefore, the request fails.

*Ref: master.md - Dictionary entry THUS (adv)*

---

## TIME (n)
- **Original:** A duration. A SHORT TIME.
- **Code-domain:** A duration or point. THE RESPONSE TIME IS 200 ms. / AT COMPILE TIME.
> **STE:** The response time is 200 ms.
> **Non-STE:** The latency is 200 ms.

*Ref: master.md - Dictionary entry TIME (n)*

---

## TIMEOUT (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A maximum wait duration. SET THE TIMEOUT TO 30 SECONDS.
> **STE:** Set the timeout to 30 seconds.
> **Non-STE:** Configure a 30-second time limit.

*Ref: Code-domain technical noun*

---

## TO (prep)
- **Original:** Function word showing direction, purpose, or connection. GO TO THE NEXT STEP.
- **Code-domain:** Function word showing direction, purpose, or connection. NAVIGATE TO THE SETTINGS PAGE. / USED TO VALIDATE DATA.
> **STE:** Navigate to the settings page.
> **Non-STE:** Go to the settings page.

*Ref: master.md - Dictionary entry TO (prep), Page 27*

---

## TOKEN (n) - (TN)
- **Original:** A symbol. Code-domain: An authentication or parsing unit.
- **Code-domain:** An authentication credential. PASS THE TOKEN IN THE AUTHORIZATION HEADER.
> **STE:** Pass the token in the Authorization header.
> **Non-STE:** Include the token in the request.

*Ref: Code-domain technical noun*

---

## TOO (adv)
- **Original:** More than necessary. TOO MUCH FORCE.
- **Code-domain:** More than necessary. TOO MANY CONNECTIONS.
> **STE:** Too many open connections.
> **Non-STE:** Excessively many open connections.

*Ref: master.md - Dictionary entry TOO (adv)*

---

## TOP (adj), TOP (n)
- **Original:** The highest part. THE TOP OF THE PAGE. / The highest. THE TOP COVER.
- **Code-domain:** The highest or first. THE TOP OF THE FILE. / THE TOP RESULT.
> **STE:** The top of the file contains the imports.
> **Non-STE:** The beginning of the file contains the imports.

*Ref: master.md - Dictionary entry TOP (adj)*

---

## TOUCH (v)
- **Original:** To make contact. DO NOT TOUCH THE HOT SURFACE.
- **Code-domain:** To modify file timestamp or access. TOUCH THE FILE TO UPDATE ITS MODIFICATION DATE.
> **STE:** Touch the file to update its modification date.
> **Non-STE:** Update the file timestamp.

*Ref: master.md - Dictionary entry TOUCH (v)*

---

## TRACK (v) - (TV)
- **Original:** To follow the path of. Code-domain technical verb.
- **Code-domain:** To monitor version control status. TRACK THE CHANGES WITH GIT.
> **STE:** Track the changes with git.
> **Non-STE:** Monitor the changes with git.

*Ref: Code-domain technical verb*

---

## TRAIN (v) - (TV)
- **Original:** To teach. Code-domain technical verb (ML).
- **Code-domain:** To fit a machine learning model. TRAIN THE MODEL ON THE TRAINING SET.
> **STE:** Train the model on the training set.
> **Non-STE:** Fit the model to the training data.

*Ref: Code-domain technical verb*

---

## TRANSFER (v)
- **Original:** To move from one place to another. TRANSFER THE DATA.
- **Code-domain:** To move data. TRANSFER THE FILE VIA SCP.
> **STE:** Transfer the file via SCP.
> **Non-STE:** Copy the file via SCP.

*Ref: master.md - Dictionary entry TRANSFER (v)*

---

## TRIGGER (v) - (TV)
- **Original:** To cause to occur. Code-domain technical verb.
- **Code-domain:** To initiate an action. THE EVENT TRIGGERS THE CALLBACK.
> **STE:** The event triggers the callback.
> **Non-STE:** The event fires the callback.

*Ref: Code-domain technical verb*

---

## TRUE (adj) - UNNAPROVED
- **Original:** CORRECT (adj). CORRECT ALIGNMENT.
- **Code-domain:** A Boolean value. THE CONDITION IS TRUE.
> **STE:** The condition is true.
> **Non-STE:** The condition evaluates to truth.

*Ref: master.md - Dictionary entry true (adj), Page 27*

---

## TRY (v)
- **Original:** To attempt. TRY THE PROCEDURE AGAIN.
- **Code-domain:** To attempt. TRY THE REQUEST AGAIN.
> **STE:** Try the request again.
> **Non-STE:** Retry the request.

*Ref: master.md - Dictionary entry TRY (v)*

---

## TURN (v)
- **Original:** To move around an axis. TURN THE KNOB.
- **Code-domain:** To change state. TURN ON THE FEATURE. / TURN OFF THE LOGGING.
> **STE:** Turn on the feature flag.
> **Non-STE:** Enable the feature flag.

*Ref: master.md - Dictionary entry TURN (v)*

---

## TYPE (n) - (TN)
- **Original:** A category. Code-domain technical noun.
- **Code-domain:** A data type. THE TYPE OF THE VARIABLE IS STRING.
> **STE:** The type of the variable is string.
> **Non-STE:** The variable is a string.

*Ref: Code-domain technical noun*

---

# U

## UNDER (prep) - UNNAPROVED
- **Original:** BELOW (prep), IN (prep), LESS THAN. BELOW THE LIMIT.
- **Code-domain:** BELOW (prep), LESS THAN. BELOW THE THRESHOLD.
> **STE:** Below the threshold.
> **Non-STE:** Under the threshold.

*Ref: master.md - Dictionary entry under (prep), Page 27, 146*

---

## UNLOCK (v)
- **Original:** To open a lock. UNLOCK THE DOOR.
- **Code-domain:** To release a resource. UNLOCK THE MUTEX.
> **STE:** Unlock the mutex.
> **Non-STE:** Release the mutex.

*Ref: master.md - Dictionary entry UNLOCK (v), Page 27*

---

## UNSTABLE (adj) - (TN)
- **Original:** Not in original STE. Code-domain technical adjective.
- **Code-domain:** Not stable; likely to fail. THE CONNECTION IS UNSTABLE.
> **STE:** The connection is unstable.
> **Non-STE:** The connection is flaky.

*Ref: Code-domain technical adjective*

---

## UNTIL (prep)
- **Original:** Up to the time that. DO THE PROCEDURE UNTIL THE PRESSURE IS STABLE.
- **Code-domain:** Up to the time that. RETRY THE REQUEST UNTIL IT SUCCEEDS.
> **STE:** Retry the request until it succeeds.
> **Non-STE:** Keep retrying the request while it fails.

*Ref: master.md - Dictionary entry UNTIL (prep)*

---

## UNUSUAL (adj)
- **Original:** Not usual. LISTEN FOR UNUSUAL NOISES.
- **Code-domain:** Not usual. WATCH FOR UNUSUAL LOG ENTRIES.
> **STE:** Watch for unusual log entries.
> **Non-STE:** Watch for unexpected log entries.

*Ref: master.md - Dictionary entry UNUSUAL (adj)*

---

## UP (adv), UP (prep)
- **Original:** In a higher position. MOVE THE LEVER UP.
- **Code-domain:** In a higher or running state. BRING THE SERVICE UP. / SCROLL UP.
> **STE:** Bring the service up.
> **Non-STE:** Start the service.

*Ref: master.md - Dictionary entry UP (adv)*

---

## UPDATE (v) - (TV)
- **Original:** To bring up to date. Code-domain technical verb.
- **Code-domain:** To change to a newer version. UPDATE THE PACKAGE TO THE LATEST VERSION.
> **STE:** Update the package to the latest version.
> **Non-STE:** Upgrade the package to the latest version.

*Ref: Code-domain technical verb*

---

## USE (v)
- **Original:** To make something do its specified function. USE THE CORRECT TOOL.
- **Code-domain:** To make a tool, API, or command do its specified function. USE THE API TO FETCH DATA.
> **STE:** Use the API to fetch data.
> **Non-STE:** Utilize the API to fetch data.

*Ref: master.md - Dictionary entry USE (v), Page 27, 420*

---

## USUAL (adj), USUALLY (adv)
- **Original:** That you use or that occurs most frequently. IF YOU DO NOT GET THE USUAL RESULTS, DO A SYSTEM TEST. / In a usual manner. USUALLY, THE HYDRAULIC FLUID FLOWS INTO THE VALVE THROUGH PORT A.
- **Code-domain:** That you expect. IF YOU DO NOT GET THE USUAL OUTPUT, CHECK THE LOGS. / MOST TIMES. USUALLY, THE REQUEST RETURNS 200 OK.
> **STE:** Usually, the request returns 200 OK.
> **Non-STE:** Typically, the request returns 200 OK.

*Ref: master.md - Dictionary entry USUALLY (adv), Page 27, 420*

---

# V

## VALID (adj) - UNNAPROVED
- **Original:** CORRECT (adj), APPLICABLE (adj). MAKE SURE THAT THE TEST RESULTS ARE CORRECT.
- **Code-domain:** CORRECT (adj). MAKE SURE THAT THE INPUT IS CORRECT.
> **STE:** Make sure that the input is correct.
> **Non-STE:** Make sure that the input is valid.

> **Note:** VALID is a technical adjective (TN) in programming (validate) per Rule 1.5.

*Ref: master.md - Dictionary entry valid (adj), Page 27*

---

## VALIDATE (v) - (TV)
- **Original:** Not in original STE. Code-domain technical verb.
- **Code-domain:** To check for correctness. VALIDATE THE USER INPUT BEFORE PROCESSING.
> **STE:** Validate the user input before processing.
> **Non-STE:** Check the user input before processing.

*Ref: Code-domain technical verb*

---

## VALUE (n)
- **Original:** A quantity that is calculated or given. MAKE SURE THAT THE VALUES AGREE WITH THE SPECIFIED TOLERANCES.
- **Code-domain:** An assigned or computed quantity. THE VALUE OF THE ENVIRONMENT VARIABLE IS "production".
> **STE:** The value of the environment variable is "production".
> **Non-STE:** The environment variable is set to "production".

*Ref: master.md - Dictionary entry VALUE (n), Page 27*

---

## VARIABLE (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** A named storage location. DECLARE THE VARIABLE BEFORE USE.
> **STE:** Declare the variable before use.
> **Non-STE:** Define the variable before use.

*Ref: Code-domain technical noun*

---

## VERIFY (v) - UNNAPROVED
- **Original:** MAKE SURE (v). MAKE SURE THAT THE FITTINGS ARE TIGHT.
- **Code-domain:** MAKE SURE (v). MAKE SURE THAT THE SIGNATURE IS CORRECT.
> **STE:** Make sure that the signature is correct.
> **Non-STE:** Verify the signature.

> **Note:** VERIFY is a technical verb (TV) in testing per Rule 1.12.

*Ref: master.md - Dictionary entry verify (v), Page 27*

---

## VERSION (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** An iteration of software. THE CURRENT VERSION IS 3.2.1.
> **STE:** The current version is 3.2.1.
> **Non-STE:** The release is 3.2.1.

*Ref: Code-domain technical noun*

---

## VERY (adv)
- **Original:** To a high degree. ADD THE OIL VERY SLOWLY.
- **Code-domain:** To a high degree. INCREASE THE VALUE VERY SLOWLY.
> **STE:** Increase the value very slowly.
> **Non-STE:** Increment the value in tiny steps.

*Ref: master.md - Dictionary entry VERY (adv), Page 422*

---

## VIA (prep) - UNNAPROVED
- **Original:** THROUGH (prep). GET ACCESS THROUGH THE No. 6 BREAK-IN PANEL.
- **Code-domain:** THROUGH (prep), BY (prep). AUTHENTICATE THROUGH OAUTH.
> **STE:** Authenticate through OAuth.
> **Non-STE:** Authenticate via OAuth.

*Ref: master.md - Dictionary entry via (prep), Page 422*

---

## VIEW (n), VIEW (v) - (TN)
- **Original:** The ability to see. MAKE SURE THAT YOU HAVE A SATISFACTORY VIEW. / To see. THE BOLT WILL BE AT THE 2 O'CLOCK POSITION WHEN SEEN FROM THE REAR.
- **Code-domain:** A display or perspective. THE LOG VIEW SHOWS RECENT ENTRIES.
> **STE:** The log view shows recent entries.
> **Non-STE:** The log display shows recent entries.

*Ref: master.md - Dictionary entry VIEW (n), Page 423*

---

## VISIBLE (adj) - UNNAPROVED
- **Original:** SEE (v), VIEW (n). MAKE SURE THAT YOU CAN SEE THE OIL LEVEL THROUGH THE SIGHT GAUGE.
- **Code-domain:** SEE (v). MAKE SURE THAT YOU CAN SEE THE OUTPUT IN THE TERMINAL.
> **STE:** Make sure that you can see the output in the terminal.
> **Non-STE:** Make sure that the output is visible in the terminal.

*Ref: master.md - Dictionary entry visible (adj), Page 28*

---

## VISUAL (adj)
- **Original:** That you can see. MAKE SURE THAT THE VISUAL INDICATOR SHOWS THE CORRECT VALUE.
- **Code-domain:** Related to display. DO A VISUAL INSPECTION OF THE UI.
> **STE:** Do a visual inspection of the UI.
> **Non-STE:** Visually inspect the UI.

*Ref: master.md - Dictionary entry VISUAL (adj), Page 28*

---

## VOLUME (n)
- **Original:** 1. The space that an object fills. MEASURE THE VOLUME OF THE OIL CAREFULLY. 2. How loud a sound is. TO ADJUST THE VOLUME, USE THE BUTTONS.
- **Code-domain:** A storage unit. MOUNT THE VOLUME TO THE CONTAINER.
> **STE:** Mount the volume to the container.
> **Non-STE:** Attach the storage to the container.

*Ref: master.md - Dictionary entry VOLUME (n), Page 424*

---

# W

## WAIT (v)
- **Original:** To stop doing something while another thing occurs. WAIT FOR 4 MINUTES.
- **Code-domain:** To block execution. WAIT FOR THE ASYNCHRONOUS TASK TO COMPLETE.
> **STE:** Wait for the asynchronous task to complete.
> **Non-STE:** Block until the async task finishes.

*Ref: master.md - Dictionary entry WAIT (v), Page 425*

---

## WANT (v)
- **Original:** To intend, to desire. RECORD THE NAME OF THE FILE THAT YOU WANT TO DOWNLOAD.
- **Code-domain:** To desire. INSTALL THE PACKAGE THAT YOU WANT.
> **STE:** Install the package that you want.
> **Non-STE:** Install the desired package.

*Ref: master.md - Dictionary entry WANT (v), Page 425*

---

## WARNING (n) - (TN)
- **Original:** A notice of danger. OBEY THE WARNINGS.
- **Code-domain:** A non-fatal notification. THE COMPILER SHOWS A WARNING.
> **STE:** The compiler shows a warning for the deprecated function.
> **Non-STE:** The compiler warns about the deprecated function.

*Ref: master.md - Dictionary entry WARNING (n), Page 425*

---

## WATCH (v) - UNNAPROVED
- **Original:** MONITOR (v), LOOK (v). MONITOR THE SPEED INDICATION. / LOOK FOR AIR BUBBLES.
- **Code-domain:** MONITOR (v). MONITOR THE LOG OUTPUT.
> **STE:** Monitor the log output for errors.
> **Non-STE:** Watch the log output for errors.

> **Note:** WATCH is a technical verb (TV) in build tools (file watcher) per Rule 1.12.

*Ref: master.md - Dictionary entry watch (v), Page 426*

---

## WE (pron)
- **Original:** The manufacturer, company, or organization that releases the documentation. WE DO NOT RECOMMEND OTHER ALTERNATIVES.
- **Code-domain:** The team that produces the documentation. WE RECOMMEND USING THE LATEST API.
> **STE:** We recommend using the latest API.
> **Non-STE:** The team recommends using the latest API.

*Ref: master.md - Dictionary entry WE (pron), Page 28, 426*

---

## WEAK (adj)
- **Original:** With small strength, power, or concentration. USE A WEAK CLEANING SOLUTION.
- **Code-domain:** With low strength. A WEAK REFERENCE DOES NOT PREVENT GARBAGE COLLECTION.
> **STE:** A weak reference does not prevent garbage collection.
> **Non-STE:** A soft reference does not prevent garbage collection.

*Ref: master.md - Dictionary entry WEAK (adj), Page 426*

---

## WEIGHT (n)
- **Original:** The force caused when gravity acts on the mass of an object. THE BASIC WEIGHT OF THE UNIT DOES NOT INCLUDE THE PROTECTIVE COVERS.
- **Code-domain:** Priority or importance. THE WEIGHT OF THE CONFIG VALUE IS 0.5.
> **STE:** The weight of the config value is 0.5.
> **Non-STE:** The priority of the config value is 0.5.

*Ref: master.md - Dictionary entry WEIGHT (n), Page 427*

---

## WHEN (conj)
- **Original:** At the time that or during. WHEN THE PISTON MOVEMENT STOPS, MEASURE THE TRAVEL.
- **Code-domain:** At the time that. WHEN THE BUILD FINISHES, DEPLOY THE ARTIFACT.
> **STE:** When the build finishes, deploy the artifact.
> **Non-STE:** After the build finishes, deploy the artifact.

*Ref: master.md - Dictionary entry WHEN (conj), Page 427*

---

## WHERE (conj)
- **Original:** At, to, or in which location. CLEAN THE AREA WHERE YOU APPLIED THE SEALANT.
- **Code-domain:** In which location. FIND THE LINE WHERE THE ERROR OCCURRED.
> **STE:** Find the line where the error occurred.
> **Non-STE:** Find the line at which the error occurred.

*Ref: master.md - Dictionary entry WHERE (conj), Page 427*

---

## WHILE (conj)
- **Original:** At the same time. MAKE SURE THAT A PERSON HOLDS THE ITEM, WHILE YOU DISCONNECT IT.
- **Code-domain:** During a period. LOG THE PROGRESS WHILE THE SCRIPT RUNS.
> **STE:** Log the progress while the script runs.
> **Non-STE:** Log the progress as the script executes.

*Ref: master.md - Dictionary entry WHILE (conj), Page 428*

---

## WHOLE (adj) - UNNAPROVED
- **Original:** FULL (adj), ALL (adj). DO THE FULL PROCEDURE. / EXAMINE ALL OF THE SYSTEM.
- **Code-domain:** ENTIRE (adj). EXAMINE ALL OF THE CODEBASE.
> **STE:** Examine all of the codebase.
> **Non-STE:** Examine the whole codebase.

*Ref: master.md - Dictionary entry whole (adj), Page 428*

---

## WIDE (adj)
- **Original:** That has a specified or large width. REPAIR ALL CRACKS THAT ARE WIDER THAN 0,05 mm.
- **Code-domain:** Broad in scope. WIDE TEST COVERAGE.
> **STE:** Wide test coverage.
> **Non-STE:** Broad test coverage.

*Ref: master.md - Dictionary entry WIDE (adj), Page 28, 429*

---

## WILL (v)
- **Original:** Auxiliary modal verb that shows simple future tense. WARNINGS AND CAUTIONS IN THIS MANUAL WILL HELP YOU TO DO THE WORK SAFELY AND CORRECTLY.
- **Code-domain:** Auxiliary modal verb for future. THE DOCS WILL HELP YOU TO SET UP THE PROJECT.
> **STE:** The docs will help you to set up the project.
> **Non-STE:** The docs are going to help you set up the project.

*Ref: master.md - Dictionary entry WILL (v), Page 28, 429*

---

## WITH (prep)
- **Original:** Function word that shows association or relationship, help or sharing, a means or instrument. ALIGN THE MARK WITH THE LONGITUDINAL AXIS.
- **Code-domain:** Function word for association or means. COMPARE THE RESULT WITH THE EXPECTED VALUE. / RUN THE SCRIPT WITH ADMIN PRIVILEGES.
> **STE:** Compare the result with the expected value.
> **Non-STE:** Compare the result against the expected value.

*Ref: master.md - Dictionary entry WITH (prep), Page 28, 430*

---

## WITHOUT (prep)
- **Original:** Not with. SMALL DAMAGE IS PERMITTED WITHOUT REPAIR.
- **Code-domain:** Not having. RUN THE BUILD WITHOUT CACHING.
> **STE:** Run the build without caching.
> **Non-STE:** Run the build with caching disabled.

*Ref: master.md - Dictionary entry WITHOUT (prep), Page 28, 430*

---

## WORK (n)
- **Original:** That which you do when you use physical strength, or mental power. DO THE WORK IN A CLEAN AREA.
- **Code-domain:** A task or effort. DO THE WORK IN A DEDICATED BRANCH.
> **STE:** Do the work in a dedicated branch.
> **Non-STE:** Do the task in a dedicated branch.

*Ref: master.md - Dictionary entry WORK (n), Page 430*

---

## WORKER (n) - (TN)
- **Original:** A person who works. Code-domain: A background process.
- **Code-domain:** A background processing unit. THE WORKER PROCESSES JOBS FROM THE QUEUE.
> **STE:** The worker processes jobs from the queue.
> **Non-STE:** The background job processor handles the queue.

*Ref: Code-domain technical noun*

---

## WRITE (v)
- **Original:** To record data or information as words, letters, or symbols. WRITE THE TEST DATE ON THE CERTIFICATE.
- **Code-domain:** To output data to storage. WRITE THE RESULT TO A FILE.
> **STE:** Write the result to a file.
> **Non-STE:** Save the result to a file.

*Ref: master.md - Dictionary entry WRITE (v), Page 431*

---

## WRONG (adj) - UNNAPROVED
- **Original:** INCORRECT (adj). IDENTIFY THE BELLCRANK AND SHAFT WITH MARKS TO PREVENT AN INCORRECT INSTALLATION.
- **Code-domain:** INCORRECT (adj). MARK THE VARIABLE TO PREVENT INCORRECT USAGE.
> **STE:** Mark the variable as private to prevent incorrect usage.
> **Non-STE:** Mark the variable as private to prevent wrong usage.

*Ref: master.md - Dictionary entry wrong (adj), Page 28, 431*

---

# X

> **Note:** The STE Dictionary has no approved or unapproved entries beginning with X. In code documentation, the letter X is used in technical noun contexts (e.g., X-axis, XML namespace, X-Forwarded-For header). These are handled as technical nouns per Rule 1.5.

*Ref: master.md - No X entries in original Dictionary*

---

# Y

## YES (adv)
- **Original:** Function word that shows the positive answer to a question. DOES THE LIGHT COME ON? YES OR NO?
- **Code-domain:** Function word for positive confirmation. DOES THE TEST PASS? YES OR NO?
> **STE:** Does the test pass? Yes or no?
> **Non-STE:** Is the test passing? Affirmative or negative?

*Ref: master.md - Dictionary entry YES (adv), Page 433*

---

## YET (conj) - UNNAPROVED
- **Original:** BUT (conj). TIGHTEN THE NUTS, BUT KEEP THEM SUFFICIENTLY LOOSE TO REMOVE THEM WITH YOUR HAND.
- **Code-domain:** BUT (conj). COMPILE THE PROJECT, BUT SKIP THE TESTS.
> **STE:** Compile the project, but skip the tests.
> **Non-STE:** Compile the project, yet skip the tests.

*Ref: master.md - Dictionary entry yet (conj), Page 28, 433*

---

## YET (adv) - UNNAPROVED
- **Original:** AT THIS TIME. DO NOT REMOVE THE FIXTURE COVER AT THIS TIME.
- **Code-domain:** AT THIS TIME. DO NOT DEPLOY THE FEATURE AT THIS TIME.
> **STE:** Do not deploy the feature at this time.
> **Non-STE:** Do not deploy the feature yet.

*Ref: master.md - Dictionary entry yet (adv), Page 28, 433*

---

## YOU (pron)
- **Original:** The reader or the user. YOU CAN CONTINUE THE TEST. HOT SURFACES CAN BURN YOU.
- **Code-domain:** The reader or the user. YOU CAN RUN THE SCRIPT. INCORRECT PERMISSIONS CAN PREVENT YOU FROM DEPLOYING.
> **STE:** You can run the script from the command line.
> **Non-STE:** The user can run the script from the command line.

*Ref: master.md - Dictionary entry YOU (pron), Page 28, 433*

---

## YOUR (adj)
- **Original:** Related to the reader or the user. IF YOU GET SOLVENT IN YOUR EYES, FLUSH THEM IMMEDIATELY WITH WATER.
- **Code-domain:** Related to the reader or the user. IF YOU GET AN ERROR IN YOUR TERMINAL, READ THE LOGS.
> **STE:** If you get an error in your terminal, read the logs.
> **Non-STE:** If an error appears in the terminal, read the logs.

*Ref: master.md - Dictionary entry YOUR (adj), Page 433*

---

# Z

## ZERO (n) - (TN)
- **Original:** Not in original STE. Code-domain technical noun.
- **Code-domain:** The numeric value 0. INITIALIZE THE COUNTER TO ZERO.
> **STE:** Initialize the counter to zero.
> **Non-STE:** Set the counter to 0.

*Ref: Code-domain technical noun; master.md entry zero (v), Page 433*

---

# Appendices & Reference

> **Note:** The source file `ste-code/merged/master.md` (extracted from ASD-STE100 Issue 9, pages 149-434) contains only the Dictionary A-Z entries. The official ASD-STE100 also includes:
> - **Change History** - tracked via the Highlights section (pages 3-28 of the spec)
> - **Change Form** - a template for submitting proposed changes to the standard
> - **Subject-to-Rule Index** - cross-references subjects to governing rules
> - **List of Approved Verbs** - quick-reference table of ~200 approved verbs (included in Dictionary intro, pages 147-148 of master.md)
> - **List of Recurring Errors** - common mistakes writers make (included in Dictionary intro, pages 145-146 of master.md)
>
> These sections were not available in the enriched files used to create `master.md`. The adaptation above covers all Dictionary A-Z entries present in the extraction.

---

## List of Recurring Errors - Code-Documentation Domain

> Adapted from master.md pages 145-146

| Non-STE | STE-Code Alternative |
|---------|---------------------|
| acceptable (adj) | PERMITTED (adj) |
| alternate (adj) | ALTERNATIVE (adj) |
| avoid (v) | PREVENT (v) |
| check (v) | VERIFY (v) or CHECK (n) with DO |
| complete (adj) | COMPLETED (adj) |
| damage (v) | DAMAGE (n) with CAUSE |
| ensure (v) | MAKE SURE (v) |
| fit (v) | INSTALL (v) |
| follow (v) | OBEY (v) |
| further (adj) | MORE (adj) |
| have to (v) | MUST (v) |
| however (adv) | BUT (conj) |
| insert (v) | PUT (v) |
| main (adj) | PRIMARY (adj) |
| may (v) | CAN (v) |
| need (v) | NECESSARY (adj) / MUST (v) |
| perform (v) | DO (v) |
| portion (n) | PART (n) |
| press (v) | PUSH (v) |
| repeat (v) | DO ... AGAIN |
| require (v) | NECESSARY (adj) / MUST (v) |
| shall (v) | MUST (v) |
| should (v) | MUST (v) |
| since (conj) | BECAUSE (conj) |
| test (v) | TEST (n) with DO |
| therefore (adv) | THUS (adv) |
| under (prep) | BELOW (prep) / IN (prep) |
| using (v) | USE (v) / WITH (prep) |

---

## Summary Statistics

- **Approved words adapted:** 452 (UPPERCASE entries)
- **Unapproved words adapted:** 108 (entries marked UNAPPROVED, with approved alternatives)
- **Total entries in this adaptation:** 560
- **Source:** ste-code/merged/master.md lines 5591-10976
- **Original specification:** ASD-STE100 Issue 9, January 2025, Part 2 - Dictionary, Pages 149-434

> Counts are measured from the `##` entry headings in this file. The source
> standard's dictionary is larger; this adaptation covers the code-relevant
> subset, so more entries are added as the pipeline runs.

---

*End of STE-Code Adapted Dictionary A-Z*
