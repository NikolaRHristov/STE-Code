================================================================================
PASTE THIS INTO THE OTHER SESSION — FULL COORDINATOR PROMPT
================================================================================

Read this file and MERGE it with your current instructions:

    instruction/STE-CODE-IMPLEMENTATION.md

If that file and your current instructions conflict, the file takes priority
for execution strategy. Your existing instructions define WHAT to build;
the file defines HOW to build it efficiently.

CRITICAL: Do NOT get confused by combined context. The file adds a parallel
execution layer — it does not change your output goals, only how you get there.

ENHANCE YOUR PROCESSING:
- Before any action, read the file and internalize its 5-phase plan
- For each worker you launch, enhance its prompt: add page-specific extraction
  hints based on what you already know about that section of the spec
- Batch your launches: 3 workers at a time, never more
- After each batch completes, pause and verify output quality before launching
  the next batch
- Enhance your own merge phase: cross-reference worker outputs for consistency,
  flag gaps, and launch correction workers for any missing data

ENHANCE YOUR THOUGHT PROCESS:
- When deciding what to adapt (Phase 2), think aloud about each category
  mapping before writing it
- For each rule adaptation, verify the original text from a worker's JSON
  before producing the STE-Code version
- If you encounter ambiguity, re-read the relevant spec page directly
  rather than guessing

START IMMEDIATELY: Read the instruction file, create the ste-code/ and
ste-code/workers/ directories, then launch Batch 1 of workers.
