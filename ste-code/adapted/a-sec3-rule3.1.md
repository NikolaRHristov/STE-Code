# Rule 3.1 — Use Only the Verb Forms That Are Given in the Dictionary

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.1

## Original Rule

Use only the verb forms that are given in the dictionary.

The STE dictionary gives you the verb forms that you can use for each approved verb.

Example:

```
REMOVE (v)
REMOVES
REMOVED,
REMOVED

GIVE (v)
GIVES
GAVE,
GIVEN
```

The introduction to the dictionary in part 2 gives you more information about the verb forms and how to use the approved verbs.

> **Source:** Issue 9, Part 1 — Writing rules, Page 1-3-1, 2025-01-15

## STE-Code Adaptation

Use only the verb forms that are given in the STE-Code approved vocabulary. Each approved verb has a fixed set of forms: the base form (infinitive), the third-person singular present form, the simple past form, and the past participle form. Do not use irregular or invented forms that are not listed for the approved verb.

The STE-Code approved vocabulary lists the verb forms for each approved verb identically to the STE dictionary convention:

```
BUILD (v)
BUILDS
BUILT,
BUILT

WRITE (v)
WRITES
WROTE,
WRITTEN
```

Only these listed forms are permitted. Never invent a past tense or past participle that is not specified. For example, if the vocabulary lists "built" as the past tense of "build," then "builded" is not permitted.

### Examples

> **Non-STE:** The compiler has builded the project with the new configuration.
> **STE:** The compiler built the project with the new configuration.

> *Adapted from spec pair: the STE dictionary gives verb forms such as REMOVE/REMOVES/REMOVED/REMOVED.* Just as STE only permits the listed verb forms for each approved verb, STE-Code only permits the listed forms. "Builded" is not an approved past tense of "build" — only "built" is permitted.

> **Non-STE:** The function writed the output to the log file.
> **STE:** The function wrote the output to the log file.

> *Adapted from spec pair: the STE dictionary gives verb forms such as GIVE/GIVES/GAVE/GIVEN.* Just as STE only permits "gave" (not "gived") as the past tense of "give," STE-Code only permits "wrote" (not "writed") as the past tense of "write."

---

## Code-Domain Explanation

Rule 3.1 is the verb-form gate of STE-Code. Every approved verb in the controlled terminology has exactly four listed forms. For every sentence in code documentation, the verb form you choose must be one of these four. You must never invent a form — not by adding a suffix, not by applying a regular pattern to an irregular verb, not by analogy with another verb. This section explains how the rule applies to each type of code documentation.

### README Files

README files use the imperative mood (base form) for procedural sections and the simple present tense for descriptive sections. Rule 3.1 requires that the base form you use in an instruction is the same base form listed first in the controlled terminology entry.

The most common Rule 3.1 violation in README files is inventing a past tense for an irregular approved verb. For example, the approved verb "run" has the listed forms RUN, RUNS, RAN, RUN. "Runned" is not listed and is not permitted. Writers sometimes apply regular "-ed" patterns to irregular verbs in README historical sections or changelogs.

Another frequent violation is inventing a "-ing" form where the controlled terminology does not list one. The verb-form convention in STE-Code does not include the "-ing" form as a listed form. Use the simple present instead of the continuous aspect: "The server runs on port 3000" not "The server is running on port 3000."

> **Non-STE:** After you have runned the setup script, the server will be running on port 8080. You can then beginned testing the endpoints.
> **STE:** After you run the setup script, the server runs on port 8080. You can then begin testing the endpoints.
> *(Rule 3.1 applied: "runned" → "run" — only RAN is the past tense of RUN. "Beginned" → "begin" — only BEGAN is the past tense of BEGIN. "Will be running" → "runs" — the simple present replaces the continuous.)*

### API Documentation

API documentation uses the simple present tense for return value descriptions and behavior specifications. The third-person singular form (the second listed form) is the most common verb form in API docs because the implied subject is the function or method name.

Rule 3.1 affects API documentation most when describing state transitions or completed operations. If you describe what a method did after it completed, you must use the approved past tense form from the controlled terminology. "The method built the response" is correct because BUILT is the listed past tense of BUILD. "The method builded the response" is incorrect.

When an API method returns a Promise or Future, the documentation describes what happens when the asynchronous operation completes. Use the approved past participle form (the fourth listed form) for describing the completed state: "The Promise gives the built response." BUILT is the listed past participle of BUILD.

> **Non-STE:** POST /api/build — Triggers a build. The endpoint returns 202 Accepted and the builded artifact is available at GET /api/build/:id.
> **STE:** POST /api/build — Starts a build. The endpoint gives a 202 Accepted status. The built artifact is available at GET /api/build/:id.
> *(Rule 3.1 applied: "builded" → "built" — only BUILT is the listed past participle of BUILD. "Triggers" → "Starts" — P1 applied. "Returns" → "gives" — P1 applied.)*

### Docstrings and Inline Comments

Docstrings use the imperative mood for the first line and the simple present tense for additional description. Rule 3.1 constrains both: the imperative must be the base form (first listed form), and the simple present must use the listed third-person singular or base form depending on the subject.

In docstrings, the most common Rule 3.1 violation is using an irregular past tense where the simple present is required. Writers sometimes describe what a function does in the past tense as if reporting a completed action: "Checked the input and returned a boolean." The correct form uses the imperative for the first line: "Check the input and give a boolean."

Inline comments often use abbreviated verb forms that do not appear in the controlled terminology. "Writen to file" is a Rule 3.1 violation — only WRITTEN is the listed past participle of WRITE. The writer must use the correct spelling from the controlled terminology.

> **Non-STE:** /**
>  * Wroten the configuration to the file system.
>  * The function readed the template and builded the output.
>  */
> **STE:** /**
>  * Write the configuration to the file system.
>  * The function reads the template and builds the output.
>  */
> *(Rule 3.1 applied: "Wroten" → "Write" — WRITTEN is the past participle, but the docstring first line uses imperative. "Readed" → "reads" — only READ (pronounced "red") is the past tense. "Builded" → "builds" — only BUILT is the past tense/past participle.)*

### Commit Messages

Commit messages use the imperative mood exclusively. The subject line must use the base form of the verb — the first listed form in the controlled terminology. Rule 3.1 reinforces the imperative-mood convention: use "add," "fix," "remove," "update," "set," "make," never the past tense forms "added," "fixed," "removed," "updated," "setted," "maked."

The past tense in a commit message subject line is a Rule 3.1 violation. "Fixed memory leak" uses the listed past tense of FIX — this is correct English but incorrect STE-Code for a commit message because commit messages use the imperative mood. Use the base form "Fix memory leak."

Some approved verbs have irregular forms where the base form and the past tense are identical: SET (v), SETS, SET, SET. "Set" is both the imperative and the past tense. In a commit message, "Set the timeout to 30 seconds" uses the imperative form, which is identical to the base form — this is correct.

> **Non-STE:** Fixed the race condition and added a timeout. The build pass and the tests runned successfully.
> **STE:** Fix the race condition and add a timeout. Make the build pass and make the tests run.
> *(Rule 3.1 applied: "Fixed" → "Fix" (imperative); "added" → "add" (imperative); "pass" used as past tense → "Make the build pass" (restructured); "runned" → "run" — RUN is both base and past participle, but "runned" is never correct.)*

### Error Messages

Error messages describe a state or a failure condition. They use the simple past tense to report what happened and the simple present tense to describe the current state. Rule 3.1 requires that the past tense form is the listed form from the controlled terminology.

The most common Rule 3.1 violation in error messages is inventing a past tense for an irregular verb that describes a system action: "The process quitted unexpectedly" uses "quitted" instead of the listed past tense "quit" (QUIT is irregular: QUIT, QUITS, QUIT, QUIT). "The connection broked" uses "broked" instead of the listed past tense "broke" (BREAK, BREAKS, BROKE, BROKEN).

Error messages written by non-native English speakers often apply regular "-ed" patterns to all verbs. Rule 3.1 prevents this by requiring the writer to check the controlled terminology for each verb's listed forms.

> **Non-STE:** ERROR: The server catched a fatal signal and shuts down. The child process runned for 0 seconds.
> **STE:** ERROR: The server caught a fatal signal and shut down. The child process ran for 0 seconds.
> *(Rule 3.1 applied: "catched" → "caught" — CATCH, CATCHES, CAUGHT, CAUGHT. "Shuts" (present tense mismatch with past context) → "shut" — SHUT is both base and past. "Runned" → "ran" — RUN, RUNS, RAN, RUN.)*

---

## Paradigm-Specific Guidance

Rule 3.1 applies to all code documentation regardless of programming paradigm. But each paradigm uses different approved verbs with different irregular patterns. This section gives guidance for the verb forms most frequently misused in each paradigm.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses approved verbs that describe class relationships, object lifecycle, and design pattern operations. Many of these verbs have irregular past forms that writers frequently apply incorrectly.

**Frequently misused OOP verb forms:**

| Base Form | 3rd Person | Past Tense | Past Participle | Common Error | Correct Use |
|-----------|------------|------------|-----------------|--------------|-------------|
| SET | SETS | SET | SET | setted | The constructor set the property. |
| GET | GETS | GOT | GOT (past only) | getted | The accessor got the value. |
| MAKE | MAKES | MADE | MADE | maked | The factory made the object. |
| KEEP | KEEPS | KEPT | KEPT | keeped | The cache kept the data. |
| SEND | SENDS | SENT | SENT | sended | The method sent the message. |
| HOLD | HOLDS | HELD | HELD | holded | The reference held the object. |
| FIND | FINDS | FOUND | FOUND | finded | The query found the record. |

The verb "get" has a special constraint: GOT is the listed past tense, but GOT is not listed as a past participle in the controlled terminology. Use "got" only for completed past actions: "The function got the data." For descriptive state, restructure: "The data is available" instead of "The data is gotten."

> **Non-STE:** The `UserRepository` finded the user record and setted the cache entry. The service keeped the connection and sended the response. The user getted the data.
> **STE:** The `UserRepository` found the user record and set the cache entry. The service kept the connection and sent the response. The user got the data.
> *(Rule 3.1 applied: "finded" → "found"; "setted" → "set"; "keeped" → "kept"; "sended" → "sent"; "getted" → "got".)*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation uses the simple present tense predominantly because pure functions describe timeless transformations. The third-person singular form (second listed form) is the most common verb form. The past tense appears rarely, usually in descriptions of evaluation order or historical context.

Code-domain technical verbs in functional programming ("map," "filter," "fold," "reduce," "compose") follow standard English morphology. They are not in the controlled terminology as approved verbs but are permitted under Rule 1.12. Their forms follow the regular pattern: MAP, MAPS, MAPPED, MAPPED; FILTER, FILTERS, FILTERED, FILTERED. The regular pattern means Rule 3.1 violations are less frequent for these technical verbs — the "-ed" suffix is indeed the correct form.

However, functional documentation does use approved verbs with irregular forms when describing what functions do: "give," "take," "do," "run," "hold," "find." These retain their irregular patterns from the controlled terminology.

> **Non-STE:** The `foldl` function taked the accumulator and the list, applyed the function to each element, and gived the final value.
> **STE:** The `foldl` function takes the accumulator and the list, applies the function to each element, and gives the final value.
> *(Rule 3.1 applied: "taked" → "takes" (simple present, not past); "applyed" → "applies"; "gived" → "gives". The functional description uses simple present tense because pure functions do not describe past events.)*

### Procedural (C, Go, Bash)

Procedural documentation uses the imperative mood for step-by-step instructions. Each step must use the base form of an approved verb. The past tense appears in descriptions of what a previous step accomplished.

The most common Rule 3.1 violation in procedural documentation is inventing a past tense for the verb "run" when describing script or program execution. RUN, RUNS, RAN, RUN — "runned" is never correct.

Another common violation is inventing a past tense for "build" when describing compilation steps. BUILD, BUILDS, BUILT, BUILT — "builded" is never correct.

In C documentation, technical verbs like "malloc," "free," "dereference," and "link" follow standard English morphology. But the surrounding prose still uses approved verbs that must follow their listed forms.

> **Non-STE:** You runned the script and it builded the binary. The linker linkt the object files and putted the binary in the build directory.
> **STE:** You ran the script and it built the binary. The linker linked the object files and put the binary in the build directory.
> *(Rule 3.1 applied: "runned" → "ran"; "builded" → "built"; "linkt" → "linked"; "putted" → "put" — PUT is irregular: PUT, PUTS, PUT, PUT.)*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes configuration state and resource definitions. The simple present tense is the dominant verb form. The past tense appears in descriptions of what a configuration did after it was applied.

Infrastructure-as-code tools introduce technical verbs like "apply," "deploy," "provision," "destroy," and "plan." These are code-domain technical verbs (Rule 1.12) and follow regular English morphology: APPLY, APPLIES, APPLIED, APPLIED; DEPLOY, DEPLOYS, DEPLOYED, DEPLOYED.

But when these same concepts are described with approved verbs in the prose, Rule 3.1 applies fully. Use "make" instead of "provision" — MADE is the listed past tense of MAKE. Use "set" instead of "configure" — SET is both the base and the past form. Use "run" instead of "execute" — RAN is the listed past tense of RUN.

> **Non-STE:** After you applyed the Terraform configuration, it builded the VPC and setted up the subnets. The deploy step runned and putted the containers in the cluster.
> **STE:** After you applied the Terraform configuration, it built the VPC and set up the subnets. The deploy step ran and put the containers in the cluster.
> *(Rule 3.1 applied: "applyed" → "applied" (technical verb, regular); "builded" → "built"; "setted" → "set"; "runned" → "ran"; "putted" → "put".)*

### Systems (Rust Ownership, C Memory Management)

Systems documentation describes ownership, lifetimes, memory layout, and concurrency. The simple present tense is the primary verb form. Systems documentation uses a dense vocabulary of technical verbs ("own," "borrow," "move," "drop," "copy," "clone") that follow standard English morphology.

The approved verbs in systems documentation that most frequently trigger Rule 3.1 violations are: "run" (RAN, not "runned"), "write" (WROTE/WRITTEN, not "writed"), "hold" (HELD, not "holded"), "keep" (KEPT, not "keeped"), "lead" (LED, not "leaded"), and "spend" (SPENT, not "spended").

In Rust documentation, the verb "drop" is a code-domain technical verb with forms DROP, DROPS, DROPPED, DROPPED. The double "p" in "dropped" follows standard English spelling rules for consonant doubling before "-ed." The verb "panic" follows: PANIC, PANICS, PANICKED, PANICKED — the "k" is added before "-ed" per standard English spelling.

> **Non-STE:** The borrow checker holded the reference until the scope ended. The thread spended 5 seconds in the critical section. The runtime catched the panic and writed the stack trace.
> **STE:** The borrow checker held the reference until the scope ended. The thread spent 5 seconds in the critical section. The runtime caught the panic and wrote the stack trace.
> *(Rule 3.1 applied: "holded" → "held"; "spended" → "spent"; "catched" → "caught"; "writed" → "wrote".)*

---

## Extended Examples

Each example pair below shows a real code documentation scenario, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — README: Installation and First Run

> **Non-STE:** The build process has taked approximately 3 minutes on a standard machine. Once you have runned the installer, you can beginned the configuration wizard. The installer setted up all necessary files and putted them in the correct locations.
> **STE:** The build process takes approximately 3 minutes on a standard machine. After you run the installer, you can begin the configuration wizard. The installer set up all necessary files and put them in the correct locations.

> **Principle applied:** Rule 3.1 (use only listed verb forms: "taked" → "takes" / "took"; "runned" → "run" / "ran"; "beginned" → "begin" / "began"; "setted" → "set"; "putted" → "put"); P4 (use approved verb forms).
> **Explanation:** Five separate Rule 3.1 violations in two sentences. TAKE, TAKES, TOOK, TAKEN — "taked" is not listed. RUN, RUNS, RAN, RUN — "runned" is not listed. BEGIN, BEGINS, BEGAN, BEGUN — "beginned" is not listed. SET, SETS, SET, SET — "setted" is not listed. PUT, PUTS, PUT, PUT — "putted" is not listed. The STE version uses simple present for the descriptive first sentence and imperative mood for the procedural second sentence, following the documentation-type conventions for README files. The verb "set up" uses the phrasal verb pattern where SET is the base form and "up" is the particle — both base and past forms of SET are "set."

### Example 2 — API Reference: Asynchronous Operation Description

> **Non-STE:** The `buildProject` method trigged the CI pipeline and retourned a Job ID. After the job completed, the result was writed to the artifact store. The client catched the completion event and feched the download URL.
> **STE:** The `buildProject` method triggers the CI pipeline and gives a Job ID. After the job completes, the system writes the result to the artifact store. The client catches the completion event and gets the download URL.

> **Principle applied:** Rule 3.1 (use only listed verb forms: "trigged" → "triggers" — the simple present is correct for API descriptions; "retourned" is not a word — use "gives"; "writed" → "writes"; "catched" → "catches"; "feched" → "gets").
> **Explanation:** API documentation uses the simple present tense to describe what a method does. The non-STE version mixes invented past forms ("trigged," "writed," "catched," "feched") with a non-English word ("retourned"). The STE version uses the listed third-person singular forms: TRIGGER is a technical verb following regular morphology (TRIGGERS). WRITE, WRITES, WROTE, WRITTEN — "writes" is the correct third-person singular. CATCH, CATCHES, CAUGHT, CAUGHT — "catches" is the correct third-person singular. GET, GETS, GOT — "gets" is the correct third-person singular. The word "retourned" appears to be an invented English word (perhaps from French "retourner") — it has no listed form and is not a technical verb. Replace with the approved verb "give."

### Example 3 — Python Docstring: Data Processing Pipeline

> **Non-STE:** def process(self, items: list) -> dict:
>     """
>     Procesed the input list and retourned a grouped dictionary.
>
>     The method splitted the items by category, countted the items
>     in each group, and builded a result dictionary. It keeped
>     the original order of the first appearance of each category.
>
>     If the input list is empty, the method gived an empty dictionary.
>     """
> **STE:** def process(self, items: list) -> dict:
>     """
>     Process the input list and give a grouped dictionary.
>
>     The method splits the items by category, counts the items
>     in each group, and builds a result dictionary. It keeps
>     the original order of the first appearance of each category.
>
>     If the input list is empty, the method gives an empty dictionary.
>     """

> **Principle applied:** Rule 3.1 (use only listed verb forms: "Procesed" → "Process" — imperative for first line; "retourned" → "give"; "splitted" → "splits"; "countted" → "counts"; "builded" → "builds"; "keeped" → "keeps"; "gived" → "gives"); P4 (use only approved verb forms: the "-ed" past tense is not appropriate for docstrings describing behavior).
> **Explanation:** This docstring shows eight Rule 3.1 violations. "Procesed" misspells the verb "process" and uses the wrong form for a docstring first line (use imperative "Process"). "Retourned" is a non-English word. "Splitted" applies the regular "-ed" pattern to SPLIT, which is irregular: SPLIT, SPLITS, SPLIT, SPLIT. "Countted" adds an unnecessary extra "t" — COUNT is regular: COUNT, COUNTS, COUNTED, COUNTED. "Builded" applies the regular pattern to BUILD — the only past/past participle form is BUILT. "Keeped" applies the regular pattern to KEEP — the only past/past participle is KEPT. "Gived" applies the regular pattern to GIVE — the only past is GAVE and the only past participle is GIVEN. The STE version uses the simple present tense throughout the descriptive portion of the docstring, which is the correct convention for Python docstrings that describe what a method does each time it is called.

### Example 4 — Commit Message (Body): Bug Investigation

> **Non-STE:** The CI pipeline catched a segmentation fault in the worker process.
> The core dump showed that a pointer was freement after it was alredy
> setted to null. The bug was introduce in commit a3f8c2.
>
> The fix adds a check before the free() call. The test suite runned
> 500 iterations without the fault reoccurring.
> **STE:** The CI pipeline caught a segmentation fault in the worker process.
> The core dump showed that a pointer was freed after it was already
> set to null. The defect was introduced in commit a3f8c2.
>
> The fix adds a check before the free() call. The test suite ran
> 500 iterations without the fault again.

> **Principle applied:** Rule 3.1 (use only listed verb forms: "catched" → "caught"; "freement" → "freed"; "setted" → "set"; "runned" → "ran"); P1 (use approved words: "already" spelling corrected; "bug" → "defect"; "reoccurring" → "again").
> **Explanation:** Four Rule 3.1 violations in a commit message body. CATCH, CATCHES, CAUGHT, CAUGHT — "catched" is not listed. "Freement" is not a word — the past participle of "free" (a code-domain technical verb for memory deallocation) is FREED, following regular English morphology. SET, SETS, SET, SET — "setted" is not listed. RUN, RUNS, RAN, RUN — "runned" is not listed. The word "alredy" is a spelling error for "already" (Rule 1.14, American English spelling). "Bug" is replaced with "defect" per P1. "Reoccurring" is replaced with the simpler "again." This example also shows an edge case: "free" as a verb in the memory-management sense is a code-domain technical verb (Rule 1.12) and follows regular morphology — FREED is correct even though it is not independently listed in the controlled terminology.

### Example 5 — Configuration File Comment: Environment Variables

> **Non-STE:** # The session timeout (in seconds). If a user has not send a request
> # within this period, the session is considered expired and the user
> # must login again. The default value was choosed based on load testing
> # that showen the average user session lasts 15 minutes.
> # SESSION_TIMEOUT=900
> **STE:** # The session timeout (in seconds). If a user does not send a request
> # in this period, the session is expired and the user
> # must log in again. The default value was chosen based on load testing
> # that showed the average user session lasts 15 minutes.
> # SESSION_TIMEOUT=900

> **Principle applied:** Rule 3.1 (use only listed verb forms: "choosed" → "chosen"; "showen" → "showed"); P1 (use approved words: "has not send" → "does not send" — restructured with approved auxiliary; "login" → "log in" — phrasal verb separation).
> **Explanation:** Two Rule 3.1 violations. CHOOSE, CHOOSES, CHOSE, CHOSEN — "choosed" is not a listed form (the past tense is CHOSE and the past participle is CHOSEN). SHOW, SHOWS, SHOWED, SHOWN (or SHOWED) — "showen" is not a listed form. The phrase "has not send" uses the approved auxiliary "has" but the wrong form of "send" — the past participle is SENT, not "send." The STE version restructures to "does not send" which uses the simple present, avoiding the auxiliary + past participle construction. "Login" as a verb is a Rule 1.2 violation ("login" is a noun) — separate into the phrasal verb "log in."

### Example 6 — Error Message: System Startup Failure

> **Non-STE:** FATAL: The database daemon could not be start. The initialization
> script finded an error in the configuration and stoppped before it
> could complete. The log file was writed to /var/log/init.log.
> Please correct the configuration and retry the startup.
> **STE:** FATAL: The database daemon could not start. The initialization
> script found an error in the configuration and stopped before it
> could complete. The log file was written to /var/log/init.log.
> Please correct the configuration and try the startup again.

> **Principle applied:** Rule 3.1 (use only listed verb forms: "finded" → "found"; "stoppped" → "stopped"; "writed" → "written"); P1 (use approved words: "retry" → "try again").
> **Explanation:** Three Rule 3.1 violations in a user-facing error message. FIND, FINDS, FOUND, FOUND — "finded" is not listed. STOP, STOPS, STOPPED, STOPPED — "stoppped" has an extra "p" (the correct spelling doubles the "p" before "-ed": STOP + P + ED). WRITE, WRITES, WROTE, WRITTEN — "writed" is not listed. The passive construction "was written" correctly uses the past participle WRITTEN. "Retry" is not an approved word — use "try again" with the approved verb "try." The word "could" in "could not start" uses the modal + base form pattern, where the base form "start" is the first listed form of START — this is correct.

---

## Edge Cases

The following scenarios show where the boundary between listed forms and acceptable usage requires careful judgment.

### Edge Case 1: The Verb "Read" — Identical Base and Past Tense Spelling

**Scenario:** The verb READ has forms READ, READS, READ (pronounced "red"), READ (pronounced "red"). The base form and the past tense/past participle are spelled identically but pronounced differently. In written documentation, context alone distinguishes the present from the past.

**Guidance:** READ is an approved verb in the controlled terminology. Its listed forms show that the past tense is spelled "read" (not "red"). In STE-Code documentation, the spelling "read" serves for both present and past. The reader determines the tense from context. To avoid ambiguity when context does not make the tense clear, add a time adverb: "The function reads the file now" vs. "The function read the file before."

Never spell the past tense as "red" (the color). "Red" is an approved adjective meaning the color, not a verb form. "The function red the file" is incorrect. Use "The function read the file."

> **Non-STE:** The parser red the input and reds each line into memory. It red the entire file before processing.
> **STE:** The parser read the input and reads each line into memory. It read the entire file before processing.
> *(Rule 3.1 applied: "red" and "reds" are not listed forms of READ. The listed forms are READ, READS, READ, READ.)*

### Edge Case 2: Technical Verbs with Irregular Patterns That Differ from the Approved Verb

**Scenario:** Some code-domain technical verbs are homographs of approved verbs but have different irregular patterns. For example, "hang" as an approved verb has forms HANG, HANGS, HUNG, HUNG. But "hang" as a technical verb (for example, a process "hangs") sometimes uses "hanged" in domain convention (though most authorities prefer "hung").

**Guidance:** When the same spelling serves as both an approved verb and a technical verb with different irregular patterns, follow the convention of the subject field for the technical use and the controlled terminology for the approved use. For "hang" in the sense of a frozen process, most style guides in the software domain prefer "hung" (consistent with the approved verb): "The process hung." When the domain convention clearly differs and is widely established, the technical convention takes priority over the controlled terminology for the technical use only.

> **Non-STE:** The process hanged at 45% and did not respond. The debugger catched the hang condition.
> **STE:** The process hung at 45% and did not respond. The debugger caught the hang condition.
> *(Rule 3.1 applied: Both the approved verb HANG and the technical verb "hang" use HUNG as the past tense. "Hanged" is not correct in either context. "Catched" → "caught" per CATCH, CATCHES, CAUGHT, CAUGHT.)*

### Edge Case 3: Past Participle vs. Simple Past for Verbs with Different Forms

**Scenario:** Some approved verbs have different simple-past and past-participle forms. For example, BEGIN, BEGINS, BEGAN, BEGUN. The simple past is BEGAN. The past participle is BEGUN. Writers sometimes confuse which form to use in compound verb constructions.

**Guidance:** Use the simple past (third listed form) for completed past actions: "The build began at 10:00." Use the past participle (fourth listed form) with auxiliary verbs ("has," "have," "had," "is," "was," "were," "been"): "The build has begun." Never use the simple past with an auxiliary: "The build has began" is incorrect — only "has begun" is correct.

Other verbs with distinct simple-past and past-participle forms include: WRITE (WROTE vs. WRITTEN), GIVE (GAVE vs. GIVEN), SEE (SAW vs. SEEN), TAKE (TOOK vs. TAKEN), BREAK (BROKE vs. BROKEN), SPEAK (SPOKE vs. SPOKEN), CHOOSE (CHOSE vs. CHOSEN).

> **Non-STE:** The deployment has began and the script has wrote the configuration. The operator had spoke to the team before the change took effect.
> **STE:** The deployment has begun and the script has written the configuration. The operator had spoken to the team before the change took effect.
> *(Rule 3.1 applied: "has began" uses the simple past BEGAN with an auxiliary — must use past participle BEGUN. "Has wrote" uses the simple past WROTE with an auxiliary — must use WRITTEN. "Had spoke" uses the simple past SPOKE — must use SPOKEN.)*

### Edge Case 4: The "-ing" Form for Technical Nouns vs. Verb Phrases

**Scenario:** The "-ing" form is not a listed verb form in the controlled terminology. But the "-ing" form does appear in code-domain technical nouns like "logging," "caching," "routing," "debugging," "parsing," "encoding," and "scheduling." The boundary between a technical noun and a verb phrase using an unlisted "-ing" form can be ambiguous.

**Guidance:** When the "-ing" form is a recognized code-domain technical noun (it appears in the project glossary or is a standard term in the domain), it is permitted under Rule 1.5 as a technical noun. When the "-ing" form is part of a continuous-aspect verb phrase ("is running," "was building"), it is not permitted because the continuous "-ing" is not a listed verb form in the controlled terminology.

The test: can you replace the "-ing" form with a listed verb form without losing technical meaning? If yes, it is a verb use — replace it. If the "-ing" form is the name of a concept, module, or feature, it is a noun use — it stays.

> **Non-STE:** The logging module is logging all requests. The caching layer is caching database results.
> **STE:** The logging module logs all requests. The caching layer caches database results.
> *(Rule 3.1 applied: "is logging" as a verb phrase → "logs" (simple present). "Logging" as a noun modifier in "logging module" → permitted. "Is caching" as a verb phrase → "caches." "Caching" as a noun modifier in "caching layer" → permitted.)*

### Edge Case 5: American vs. British Irregular Past Forms

**Scenario:** Some irregular verbs have different past-tense and past-participle forms in American English vs. British English. For example, "learn" → "learned" (American) vs. "learnt" (British). "Spell" → "spelled" (American) vs. "spelt" (British). "Burn" → "burned" (American) vs. "burnt" (British). Rule 1.14 requires American English spelling. Does this extend to irregular verb forms?

**Guidance:** Yes. Use the American English irregular forms consistently. LEARN, LEARNS, LEARNED, LEARNED — "learnt" is not a listed form in the STE-Code controlled terminology and violates Rule 1.14. SPELL, SPELLS, SPELLED, SPELLED — "spelt" is not a listed form. BURN, BURNS, BURNED, BURNED — "burnt" is not a listed form.

For verbs like "get" where the American past participle differs (GOTTEN in American English vs. GOT in British English): the controlled terminology lists GOT as the only past form and does not list GOTTEN. Use "got" for simple past only. For past participle constructions, restructure the sentence to avoid the need for "gotten": "The data was obtained" is not STE. Use "The system got the data" (simple past) or "The data is available."

> **Non-STE:** The model learnt the patterns and burnt through the dataset. The developer had gotten the results and spilt the coffee.
> **STE:** The model learned the patterns and burned through the dataset. The developer got the results.
> *(Rule 3.1 applied: "learnt" → "learned"; "burnt" → "burned"; "had gotten" → "got" (simple past restructured); "spilt" → not applicable — remove the non-technical detail.)*

---

## Cross-References

This rule is the first rule in Section 3 (Verbs) of the STE-Code specification. It is the verb-form authority: every other rule in Section 3 depends on the correct identification and use of the listed verb forms. It also interacts closely with the Section 1 rules that define the vocabulary and its constraints.

| Rule | Title | Relationship to Rule 3.1 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs | Determines which verbs are available for use. Rule 3.1 then constrains which forms of those verbs may be used. A verb must pass Rule 1.1 before Rule 3.1 applies. |
| **Rule 1.2** | Use Approved Words Only as the Specified Part of Speech | Ensures that a word used as a verb is indeed approved as a verb. Rule 3.1 then constrains the morphological form of that verb. Together they ensure the correct part of speech (Rule 1.2) and the correct form (Rule 3.1). |
| **Rule 1.3** | Use Approved Words Only with Their Approved Meanings | Constrains the meaning of each approved verb. Rule 3.1 constrains the form. The same meaning expressed in the correct form is the goal of both rules together. |
| **Rule 1.4** | Use Only the Approved Forms of Verbs and Adjectives | The general morphological rule covering both verbs and adjectives. Rule 3.1 is the verb-specific application of Rule 1.4. Rule 1.4 defines the four-form model and the three-form adjective model broadly. Rule 3.1 applies the four-form model to every verb in every sentence of code documentation. Rule 1.4 is the rule; Rule 3.1 is the operational discipline of checking the dictionary before using any verb form. |
| **Rule 1.5** | You Can Use Words That You Can Include in a Technical Noun Category | Defines technical noun categories. Technical nouns are not verbs, so Rule 3.1 does not directly apply. But when a technical noun is verbed (a Rule 1.7 violation), the invented verb form is always a Rule 3.1 violation because it has no listed form. |
| **Rule 1.7** | Do Not Use Technical Nouns as Verbs | Forbids verbing technical nouns. Every violation of Rule 1.7 is also a violation of Rule 3.1 because the verbed technical noun has no listed verb forms. |
| **Rule 1.12** | Technical Verbs Are Allowed | Permits code-domain technical verbs. These verbs are not in the controlled terminology, so their forms are not directly listed. Rule 3.1 applies indirectly: technical verbs must follow standard English morphology. The discipline of Rule 3.1 — consult the authority before using a form — extends to checking standard English references for technical verb forms. |
| **Rule 1.13** | Do Not Use Technical Verbs as Nouns | Forbids using technical verbs as nouns. When a technical verb is nouned, its verb forms are no longer relevant to Rule 3.1. But the reverse — using a noun form of a technical verb as if it were a verb — triggers Rule 3.1 because the noun form has no listed verb forms. |
| **Rule 1.14** | Use American English Spelling | Requires American English spelling for all words. For verbs, this means using American irregular past forms (LEARNED not "learnt," SPELLED not "spelt," BURNED not "burnt") and American preferred forms where a verb has regional variants. Rule 3.1's listed forms reflect American English spelling. |

**Section 3 rule chain:** Rule 3.1 (verb forms) is the foundation. Rule 3.2 (verb tenses) builds on Rule 3.1 by specifying which of the four forms to use in each tense context. Rule 3.3 (active vs. passive voice) builds further by specifying voice. Rule 3.4 (imperative mood) specifies when to use the base form (first listed form) for instructions. Rule 3.5 (helping verbs) governs auxiliary verb use with the listed forms. Each subsequent Section 3 rule assumes the writer has already selected a listed verb form per Rule 3.1.

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. Each approved verb entry lists its four forms in the standard convention: BASE (v), 3RD PERSON SINGULAR, SIMPLE PAST, PAST PARTICIPLE. The four-form listing is the complete set of permitted forms for that verb.

**Key dictionary entries referenced in this rule:**

- **BUILD (v), BUILDS, BUILT, BUILT:** All four forms are listed. BUILT serves as both simple past and past participle. "Builded" is not a listed form.
- **WRITE (v), WRITES, WROTE, WRITTEN:** The simple past (WROTE) differs from the past participle (WRITTEN). Do not confuse them: "The function wrote the file" (past) vs. "The file was written" (participle).
- **RUN (v), RUNS, RAN, RUN:** The base form and the past participle are identical (RUN). The simple past is RAN. "Runned" is not a listed form.
- **GIVE (v), GIVES, GAVE, GIVEN:** The simple past (GAVE) differs from the past participle (GIVEN). "Gived" is not a listed form for either.
- **SET (v), SETS, SET, SET:** All three non-base forms are identical to the base form. "Setted" is not a listed form and is never correct.
- **PUT (v), PUTS, PUT, PUT:** Same pattern as SET. "Putted" is not a listed form.
- **GET (v), GETS, GOT, GOT:** GOT serves as the simple past. The past participle is also listed as GOT. The American English form "gotten" is not a listed form.

---

## Grammar Notes

### The Four-Form Listing Convention

Rule 3.1 is inseparable from the dictionary listing convention. The controlled terminology uses a specific four-line format for every approved verb:

```
VERB (v)
VERB+s
PAST,
PAST PARTICIPLE
```

The first line gives the base form with the part-of-speech tag "(v)." This base form serves as the infinitive ("to build"), the imperative mood ("Build the project"), and the simple present tense with all subjects except third-person singular ("I build, you build, we build, they build").

The second line gives the third-person singular present form. For most verbs, this is the base form + "s" (BUILDS, WRITES, GIVES, SETS). For verbs that end in "-s," "-sh," "-ch," "-x," or "-z," the form uses "-es" (CATCHES, FIXES, FINISHES). For verbs that end in a consonant + "y," the "y" changes to "i" before "-es" (CARRIES, STUDIES, TRIES). The dictionary lists the exact spelling.

The third line gives the simple past tense, followed by a comma. The comma is a convention that visually separates the past from the past participle, but it also signals that the next line is the fourth form. For regular verbs, the simple past ends in "-ed" (COMPILED, STARTED, CHECKED). For irregular verbs, the dictionary gives the exact irregular form (BUILT, WROTE, RAN, GAVE, CAUGHT, FOUND).

The fourth line gives the past participle. For regular verbs, this is identical to the simple past (COMPILED, STARTED, CHECKED). The dictionary lists it a second time to confirm that both the past-tense use and the participle use are approved. For irregular verbs, the past participle may differ from the simple past (WRITTEN vs. WROTE, GIVEN vs. GAVE, BEGUN vs. BEGAN, RUN vs. RAN).

The comma after the third line and the absence of a comma after the fourth line is a visual convention inherited from ASD-STE100. It tells the reader: "This verb has the listed simple past and the listed past participle. If the same word appears twice (BUILT, BUILT), it serves both roles. If different words appear (WROTE, WRITTEN), each serves its own role."

### The Dictionary as the Sole Authority

Rule 3.1 establishes a fundamental principle: the dictionary is the only authority for verb forms. The writer must not rely on intuition, analogy, or pattern recognition. If the dictionary lists BUILT as the past tense of BUILD, the writer must use BUILT even if the regular "-ed" pattern suggests "builded."

This principle is more important for code documentation than it appears. Many software developers are non-native English speakers who learned English grammar rules but not the extensive list of irregular verbs. The regular "-ed" pattern is the most natural for these writers. Rule 3.1 forces them to consult the controlled terminology and use the listed form, which prevents the most frequent verb-form errors in code documentation.

The dictionary-as-authority principle also prevents native English speakers from using dialectal or regional verb forms. A British English speaker might naturally write "learnt" or "spelt." Rule 3.1 directs them to the dictionary, where the listed forms are LEARNED and SPELLED (American English per Rule 1.14).

### Modal Verb + Base Form Pattern

When an approved modal verb ("can," "must," "shall" — where approved by the documentation type) appears before a main verb, the main verb must be in its base form (the first listed form). This pattern is consistent with standard English grammar and with Rule 3.1.

The modal + base form pattern is: `[modal] [base form]`

- "You can build the project." (BUILD is the base form — correct)
- "You can built the project." (BUILT is the past/past participle — incorrect after a modal)
- "You must write the data." (WRITE is the base form — correct)
- "You must wrote the data." (WROTE is the past tense — incorrect after a modal)

This pattern is especially important in procedural documentation where modals appear in conditional instructions: "If the build fails, you must check the error log." CHECK is the base form of the approved verb.

### Verb Forms in Compound Tenses

English compound tenses use an auxiliary verb plus a main verb form. Rule 3.1 governs the form of the main verb:

- **Present perfect:** `has/have + past participle (4th form)`. "The build has completed" (COMPLETED is the 4th form). "The build has complete" is incorrect — COMPLETE is the base form, not the past participle.

- **Past perfect:** `had + past participle (4th form)`. "The build had completed before the test ran."

- **Future with "will":** `will + base form (1st form)`. "The build will complete at 10:00." "The build will completed" is incorrect — COMPLETED is the past/past participle, not the base form.

- **Passive voice:** `is/was/were/been + past participle (4th form)`. "The file was written." "The file was wrote" is incorrect — WROTE is the simple past, not the past participle.

The most common error in compound tenses is using the simple past instead of the past participle after an auxiliary: "has began" instead of "has begun," "was wrote" instead of "was written," "had took" instead of "had taken." Rule 3.1 prevents this error by requiring the writer to check which form is the past participle (the 4th line) and use only that form after auxiliaries.

### The "-ing" Form: Explicit Exclusion

The "-ing" form is not one of the four listed verb forms in the controlled terminology. This is an explicit exclusion, not an oversight. The original ASD-STE100 does not list the "-ing" form for any verb, and STE-Code follows the same convention.

The exclusion of the "-ing" form means that the continuous aspect (progressive tenses) is not available in STE-Code prose. The continuous aspect uses "is/are/was/were + -ing form": "is running," "was building," "were checking." These constructions are grammatically correct English but they are not permitted in STE-Code.

The simple present tense replaces the present continuous: "The server runs" not "The server is running." The simple past replaces the past continuous: "The server ran" not "The server was running."

The "-ing" form survives in STE-Code only as part of code-domain technical nouns: "logging," "caching," "routing," "parsing," "encoding," "scheduling." In these cases, the "-ing" form is a noun, not a verb form, and it is permitted under Rule 1.5 (technical nouns).

### Interaction with Phrasal Verbs

Phrasal verbs (verb + particle, for example, "set up," "log in," "shut down") are common in code documentation. Rule 3.1 applies to the verb component of the phrasal verb. The particle is not inflected.

For the phrasal verb "set up": SET is the verb. Its forms from the controlled terminology are SET, SETS, SET, SET. All forms are identical. "Set up the server" (imperative), "The script sets up the server" (3rd person), "The script set up the server" (past) — all correct because SET is the same in all four forms.

For the phrasal verb "log in": LOG is the verb (code-domain technical verb). Its forms follow regular morphology: LOG, LOGS, LOGGED, LOGGED (with consonant doubling before "-ed"). "Log in" (imperative), "The user logs in" (3rd person), "The user logged in" (past).

When phrasal verbs use an approved verb with irregular forms, the irregular forms apply: "shut down" uses SHUT, SHUTS, SHUT, SHUT — "The system shut down" (past) is correct. "The system shutted down" is not correct — "shutted" is not a listed form.

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 3.1 is the opening rule of Section 3 (Verbs). The aerospace specification devotes Rule 3.1 to the dictionary convention for listing verb forms and to the discipline of consulting the dictionary before using any verb form. The rule is short — four paragraphs in the Issue 9 text — but it carries heavy weight because every subsequent rule in Section 3 assumes the writer has selected a listed verb form.

The aerospace justification for Rule 3.1 is safety through precision. In aircraft maintenance documentation, an incorrect verb form can change the meaning of an instruction. "The pin was removed" (passive, past participle, correct) describes a state. "The pin was remove" (base form used as past participle, incorrect) is ambiguous and could be misread as an instruction. The discipline of always using the listed forms prevents this ambiguity.

In code documentation, the same safety principle applies in a different form. An incorrect verb form in an API description can mislead a developer about what a function does. "The method builded the response" suggests an invented operation. "The method built the response" uses the correct listed form and is unambiguous. An incorrect verb form in an error message can confuse a user about what happened. "The connection broked" is harder for a non-native reader to parse than "The connection broke." The discipline of Rule 3.1 prevents these comprehension failures.

The original ASD-STE100 also notes that the introduction to the dictionary (Part 2) provides detailed guidance on reading and applying the verb-form listings. STE-Code follows the same pattern: the controlled terminology (`a-dictionary.md`) includes an introduction that explains the listing convention, and Rule 3.1 directs the writer to that introduction for detailed guidance.
