================================================================================
PASTE THIS INTO THE OTHER SESSION — GRANULAR COORDINATOR PROMPT
================================================================================

MERGE these instructions with your current behavior. The file below takes
priority for execution strategy. Your existing goals define WHAT to build —
this file defines HOW to build it with hard verification gates.

Read this file completely before taking any action:

    instruction/STE-CODE-IMPLEMENTATION.md

CRITICAL RULES (from the file — internalize these):

1. Every phase has a HARD GATE. You MUST verify file existence before
   proceeding past a gate. No gate = no progress.
2. You MUST NOT write any output artifact until the corresponding
   worker JSON exists AND the gate check passes.
3. If a worker fails or produces empty output, re-launch it.
   Do not fabricate data.
4. Track ALL progress in ste-code/PROGRESS.md — update it after
   every single completed step. Checkboxes start as [ ] and become [x].
5. All STE-Code output MUST cross-reference data from worker JSONs.
   If the data isn't in a worker file, you don't have it yet.

EXECUTION ORDER (DO NOT SKIP STEPS):

Step 0: GATE 0 — Verify spec files, create directories, init PROGRESS.md
Step 1: GATE 1 — Launch workers in 3 batches, verify each batch
Step 2: GATE 2 — Merge to master.json, spot-check 10 pages
Step 3: GATE 3 — Adapt every rule, category, synonym, polysemy entry
Step 4: GATE 4 — Write 6 artifact files, verify token budgets

At each gate, run the verification commands provided in the file.
If a gate fails, STOP and fix the problem. Do not proceed.

ENHANCE WORKER PROMPTS:
- For each worker, include page-specific hints about what to look for
  (e.g., "W5: pages 121-180 contain the polysemy resolution table —
  look for words like FOLLOW, TEST, REPLACE with their approved meanings")
- Increase the worker prompt's specificity based on what you already
  know about that section of the spec

START: Read the instruction file now. Begin at GATE 0.
