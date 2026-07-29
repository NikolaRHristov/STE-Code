
manual_part3 = r"""
═══════════════════════════════════════════════════════════════════════════════
SECTION 6: RECURSIVE QUESTIONING PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

6.1 THE SELF-QUESTIONING LOOP
On every turn, before producing output, the agent asks itself these
questions IN ORDER. Each question either triggers an action or confirms
a state. This is the recursive engine that drives extraction.

QUESTION 1: "Have I read page current_page?"
  → If NO: Read it now (Go to S3, STEP B).
  → If YES: Continue to Q2.

QUESTION 2: "What type of page is this?" (Classify per S3.3)
  → TYPE A (Rule): Go to Q3.
  → TYPE B (Dictionary): Go to Q4.
  → TYPE C (Example): Go to Q5.
  → TYPE D (Reference): Go to Q6.
  → TYPE E (Category): Go to Q7.

QUESTION 3 (for TYPE A — Rule pages):
  3a. "What is the rule number and text?" → Extract to skills.
  3b. "What are the STE and non-STE examples?" → Extract to skills.
  3c. "Does this page contain entities (nouns) that could be UML classes?" 
      → Extract to UML.
  3d. "Does this page contain relationships (prepositional phrases)?"
      → Extract to UML.
  3e. "Does this page contain procedural steps?" → Extract to flowchart.
  3f. "Does this page contain conditions (if-then)?" → Extract to flowchart.
  3g. "Does this page contain safety instructions?" → Extract to guards.
  3h. "Are there STE violations in the examples?" → Record in violations.
  Go to Q8.

QUESTION 4 (for TYPE B — Dictionary pages):
  4a. "What words are on this page?" → Extract each to skills.
  4b. "For each word: what is its POS, meaning, and approved forms?"
      → Record in skill content.
  4c. "Is this word polysemous?" → If yes, extract polysemy resolution skill.
  4d. "Is this word unapproved with an alternative?" 
      → Extract synonym elimination skill.
  4e. "Could any word on this page be a UML class or attribute?"
      → Extract to UML.
  Go to Q8.

QUESTION 5 (for TYPE C — Example pages):
  5a. "What is the non-STE input?" → Record original.
  5b. "What is the STE output?" → Record corrected.
  5c. "Which rules were applied?" → Record rule list.
  5d. "How many transformation passes?" → Record pass count.
  5e. "What is the word count before/after?" → Record optimization.
  5f. "Can this transformation be generalized into a reusable skill?"
      → If yes, extract skill with trigger pattern.
  Go to Q8.

QUESTION 6 (for TYPE D — Reference pages):
  6a. "What structural information is here?" → Record in knowledge_fragments.
  6b. "Are there cross-references to specific rules?" → Record mapping.
  6c. "Is there a change history or version info?" → Record in knowledge.
  6d. "Does this page establish the total page count?" → Set total_pages.
  Go to Q8.

QUESTION 7 (for TYPE E — Category pages):
  7a. "What is the category number and name?" → Extract to skills.
  7b. "What example words are listed?" → Extract to skills.
  7c. "Could any example word be a UML entity?" → Extract to UML.
  Go to Q8.

QUESTION 8: "Have I extracted all skills from this page?"
  → If NO: Re-read page, return to the applicable question (Q3-Q7).
  → If YES: Continue to Q9.

QUESTION 9: "Have I extracted all UML elements from this page?"
  → If NO: Re-read page, look for nouns, relationships, procedures.
  → If YES: Continue to Q10.

QUESTION 10: "Have I recorded all violations and optimizations?"
  → If NO: Scan page again for STE non-compliance.
  → If YES: Continue to Q11.

QUESTION 11: "Have I updated all counters?"
  → Increment total_violations, total_fixes, words_original, words_corrected,
    skills_extracted, uml_elements.
  → Continue to Q12.

QUESTION 12: "Is current_page the last page?"
  → If NO: Increment current_page. Go to Q1 (RECURSIVE LOOP).
  → If YES: Go to Q13.

QUESTION 13: "Am I ready to produce the final consolidated output?"
  → If NO: Identify what is missing. Re-read pages as needed.
  → If YES: Go to S7, FINAL OUTPUT FORMAT.

6.2 RECURSIVE SELF-CORRECTION
If at any point the agent finds that a previously extracted skill contradicts
new information on the current page, the agent must:
  1. Flag the contradiction.
  2. Re-read the earlier page.
  3. Determine which interpretation is correct based on the specification.
  4. Update the skill with the correct information.
  5. Record the correction in the optimization log.

═══════════════════════════════════════════════════════════════════════════════
SECTION 7: OUTPUT FORMAT
═══════════════════════════════════════════════════════════════════════════════

7.1 PER-TURN OUTPUT (EVERY TURN EXCEPT FINAL)
After processing each page, output:

══════════ TURN N OUTPUT ══════════
PAGE: [current_page] of [total_pages]
PAGE TYPE: [A/B/C/D/E]

SKILLS EXTRACTED THIS TURN:
  [List of skills with skill_id, trigger, content, source]

UML ELEMENTS THIS TURN:
  Classes: [list]
  Relationships: [list]
  Procedures: [list]
  Conditions: [list]
  Safety: [list]

VIOLATIONS FOUND: [count]
OPTIMIZATIONS APPLIED: [count]

CUMULATIVE STATE:
  Pages processed: [N] of [total]
  Total skills: [N]
  Total UML elements: [N]
  Total violations: [N]
  Total fixes: [N]
  Words: [original] → [corrected] ([%] reduction)

NEXT ACTION: Reading page [N+1]
═════════════════════════════════

7.2 FINAL OUTPUT (LAST TURN ONLY)
After all pages are processed, output:

══════════ FINAL CONSOLIDATED OUTPUT ══════════
DOCUMENT: [title]
PAGES PROCESSED: [N]

═══ SKILL LIBRARY ═══
[Complete list of all extracted skills, organized by type:
 rules, dictionary, transformations, polysemy, synonyms, categories]

═══ UML CLASS DIAGRAM ═══
[Complete Mermaid classDiagram with all classes and relationships]

═══ UML FLOWCHART ═══
[Complete Mermaid flowchart with all procedures, conditions, safety guards]

═══ VIOLATION REPORT ═══
[All violations found across all pages, with fixes applied]

═══ OPTIMIZATION SUMMARY ═══
Total violations: [N]
Total fixes: [N]
Word reduction: [original] → [corrected] ([%] reduction)
Skills extracted: [N]
UML elements: [N]

═══ STE COMPLIANCE CERTIFICATE ═══
Document: [title]
Compliance status: [STE-compliant | N violations remain]
Assessed by: STE Self-Reading Agent v1.0
Date: [ISO 8601]
═══════════════════════════════════════════════

7.3 OUTPUT LANGUAGE
ALL output must conform to the 14 core STE principles (S1).
The agent must not produce non-STE text in any section of its output.
If the agent detects non-STE text in its own output, it must correct it
before presenting the output to the user.

═══════════════════════════════════════════════════════════════════════════════
SECTION 8: CONTEXT WINDOW MANAGEMENT
═══════════════════════════════════════════════════════════════════════════════

8.1 WHAT TO KEEP IN CONTEXT (PERSISTENT):
  - This manual (SSRM) — always in context.
  - extraction_state — the growing arrays of skills, UML, violations.
  - counters — the running totals.
  - current_page and total_pages.

8.2 WHAT TO DISCARD AFTER EACH TURN:
  - The raw page text read during the turn (free the context).
  - Intermediate analysis that has been extracted to skills or UML.
  - Do not keep raw pages in context. Only keep extracted knowledge.

8.3 CONTEXT BUDGET:
  - Manual: ~7,000 tokens (this file)
  - System prompt: ~1,200 tokens (ste_distilled_system_prompt.txt)
  - Per-turn page text: ~2,000-4,000 tokens
  - Per-turn output: ~500-1,000 tokens
  - Extraction state grows but is structured (compact format)
  - Estimated capacity: 100+ pages in a 128K context window
  - For larger documents: checkpoint state to file, reset context, reload

8.4 CHECKPOINT PROTOCOL (for large documents):
  After every 20 pages:
    1. Write extraction_state to a checkpoint file (JSON).
    2. Clear the context window.
    3. Reload this manual + system prompt + checkpoint file.
    4. Continue from current_page.

═══════════════════════════════════════════════════════════════════════════════
END OF STE SELF-READING MANUAL (SSRM) v1.0
═══════════════════════════════════════════════════════════════════════════════
"""

with open("output/ste_self_reading_manual.txt", "a") as f:
    f.write(manual_part3)

# Calculate total size
import os
total_size = os.path.getsize("output/ste_self_reading_manual.txt")
total_chars = sum(1 for _ in open("output/ste_self_reading_manual.txt"))
print(f"Manual complete. Total size: {total_size:,} bytes, ~{total_chars:,} chars")
print(f"Token estimate: ~{total_chars // 4:,} tokens")
