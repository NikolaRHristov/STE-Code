# Rule 5.1 — Short Sentences (Maximum 20 Words)

## Original Rule Summary

Rule 5.1 requires that every sentence in procedural text uses a maximum of 20 words. Long sentences in work steps are difficult to understand, especially when the reader must follow instructions while performing a task. Warnings, cautions, and safety instructions must also obey the 20-word limit. Notes are an exception — they give information only and may use up to 25 words per sentence.

## STE-Code Adaptation

Rule 5.1 in STE-Code applies the 20-word sentence limit to all procedural code documentation: installation steps, setup instructions, deployment checklists, debugging workflows, and API usage guides. Break long procedural sentences into shorter sentences that each focus on one part of the task. Warnings about security, data loss, or system stability must also obey the 20-word limit. Notes in code documentation may use up to 25 words. Code snippets, command examples, terminal output, string literals, and identifier names inside code blocks are excluded from the word count.

## Example Pairs

> **Non-STE:** Run the database migration script from the project root directory and then restart the application server to apply all pending schema changes to the production environment. (27 words)
>
> **STE:** Run the database migration script from the project root directory. (9 words) Then, restart the application server to apply all pending schema changes. (13 words)

> **Non-STE:** Build the Docker image using the Dockerfile in the project root and then run a container from that image with port 8080 on the host mapped to port 80 inside the container. (33 words)
>
> **STE:** Build the Docker image. (4 words) Use the Dockerfile in the project root. (8 words) Then, run a container from that image. (9 words) Map port 8080 on the host to port 80 inside the container. (15 words)

> **Non-STE:** The deployment pipeline will automatically run the full test suite on every push to the main branch and if all tests pass it will build a production Docker image and push it to the container registry before updating the Kubernetes deployment with the new image tag. (44 words)
>
> **STE:** The deployment pipeline runs the full test suite on every push to the main branch. (17 words) If all tests pass, the pipeline builds a production Docker image. (13 words) Then, it pushes the image to the container registry. (11 words) Finally, it updates the Kubernetes deployment with the new image tag. (14 words)

## Principles Applied

**P1** — Use approved words from the controlled terminology. Short, approved words make it easier to stay within the 20-word limit.

**P4** — Write one topic per descriptive sentence. Each sentence addresses a single subject, keeping the word count low and the meaning clear.

**P5** — Write one instruction per procedural step. Each work step describes exactly one action, making it natural for each sentence to stay under 20 words.

**P7** — Use the imperative mood for all procedural writing. Imperative sentences drop the subject ("Run the script" instead of "You must run the script"), removing one or two words per sentence.

**P13** — Do not use semicolons to join independent clauses. Use a period and start a new sentence. This prevents compound sentences that exceed the 20-word limit.
