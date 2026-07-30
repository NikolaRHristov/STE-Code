# Rule 8.5 — Parentheses and Word Count

> **Source:** ASD-STE100 Issue 9, Rule 8.5 · Level 5 Summary

## Original Rule Summary

Rule 8.5 governs word counting when parentheses appear in a sentence. Text between parentheses counts as a single word in the enclosing sentence, regardless of how many words it contains internally. The words inside the parentheses form their own separate sentence with its own word-count limit. Identifiers (numbers, letters, alphanumeric codes) and abbreviations placed in parentheses also count as one word each.

## STE-Code Adaptation

In code documentation, parentheses serve as a tool for managing sentence length without sacrificing completeness. When a sentence approaches the 20-word procedural or 25-word descriptive limit, moving qualifying information into parentheses reduces the main sentence's word count by the length of the moved text minus one. The parenthetical text remains a separate sentence and must independently obey the same word-count limits. Parentheses must never be used to bury safety preconditions, warnings, or required steps—critical information belongs in its own sentence or a labeled block (BREAKING, DEPRECATED, NOTE).

## Example Pairs

> **Non-STE:** Make sure that the DEBUG environment variable is set to false before you run the deployment script in the production cluster (the DEBUG flag must be explicitly disabled for all production workloads to prevent accidental log leakage).
>
> **STE:** Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off). (12 words)
>
> *The main sentence has 12 words because the parenthetical counts as one word. The parenthetical sentence has 5 words. The original parenthetical embedded 10 words of rationale. Moving qualifying text to a short parenthetical keeps the main sentence under the procedural limit while the aside remains independently brief.*

> **Non-STE:** Failed to bind to port 8080 because the address is already in use by another process that was started previously and is still holding the socket open on that port number (you can identify the process using the lsof -i :8080 command and then terminate it with kill followed by the process ID, or you can configure this application to use a different port by setting the PORT environment variable to an alternative value such as 3000 or 9090 before restarting).
>
> **STE:** Cannot bind to port 8080 (EADDRINUSE). The address is in use. To find the process, run `lsof -i :8080`. To use a different port, set the PORT environment variable (example: 3000). Then restart the application.
>
> *The error code parenthetical `(EADDRINUSE)` is an alphanumeric identifier—it counts as one word in the main sentence and forms a one-word separate sentence. The example value parenthetical `(example: 3000)` counts as one word. The original had a 71-word parenthetical containing both diagnostic and recovery instructions. The fix separates error identification, diagnostic steps, and recovery steps into distinct sentences with short parenthetical identifiers.*

> **Non-STE:** Call the deallocate function to free the memory (the pointer must not be null and must have been previously allocated by the allocate function — calling deallocate on a null pointer or an unallocated pointer causes undefined behavior).
>
> **STE:** Call the deallocate function to free the memory. The pointer must not be null. The pointer must have been allocated by the allocate function. If you call deallocate on a null pointer or an unallocated pointer, the behavior is undefined.
>
> *Parentheses downgrade the visual priority of the text they contain. Safety-critical preconditions and undefined-behavior warnings must never appear in parentheses—a reader scanning the documentation may skip the parenthetical. Each precondition and the warning are promoted to their own sentences where they receive full visual attention.*

## Principles Applied

- **Rule 8.5 (core):** Text in parentheses counts as one word in the enclosing sentence and forms a separate sentence with its own word-count limit.
- **P1 — Use approved words:** Replace non-approved words with STE-Code dictionary equivalents (e.g., "cannot" instead of "failed to," "make sure" for instructions).
- **P2 — Use words with approved meanings:** Each word must carry only its approved meaning from the STE-Code dictionary.
- **P3 — Use simple, direct language:** Avoid embedding complex multi-clause explanations inside parentheticals; keep parenthetical sentences as grammatically complete single clauses.
- **P5 — Technical code nouns are permitted:** Identifiers like `EADDRINUSE`, `CI/CD`, version numbers, and code tokens retain their technical form and count as one word in parentheticals.
- **Rule 3.1 — Use simple sentences:** Every parenthetical forms a separate sentence and must obey the one-subject-one-verb-one-object structure.
- **Rule 4.1 — Keep sentences short:** The 20-word procedural and 25-word descriptive limits apply to parenthetical sentences just as to main sentences.
- **Rule 8.1 — Do not use the semicolon:** Semicolons are forbidden inside parentheticals; if a parenthetical contains a semicolon, split it into two sentences.
