
methodology = r"""
================================================================================
STE EXTRACTION METHODOLOGY FOR LOCAL LLM AGENTS
A turn-by-turn protocol for parsing documents, extracting UML, and
optimizing output against the STE-Distilled rule set.
================================================================================

# PREREQUISITE
Insert the STE-DISTILLED SYSTEM PROMPT (ste_distilled_system_prompt.txt)
into the system/context layer of the local LLM before the first turn.

# DOCUMENT ON STANDBY
The agent has access to the full ASD-STE100 specification PDF at all
times via file-read tools. The agent does NOT load the full document
into context. Instead, the agent reads specific sections on demand
using targeted retrieval.

# TURN-BY-TURN EXTRACTION PROTOCOL

## TURN 0 — INITIALIZATION
Agent receives: document to analyze + this methodology.
Agent action:
  1. Read the document title, table of contents, and section headers.
  2. Identify document type (procedural, descriptive, mixed).
  3. Initialize extraction state:
     - entities: []        # UML class candidates
     - relationships: []   # UML associations
     - procedures: []      # ordered step sequences
     - conditions: []      # if-then blocks
     - safety: []          # precondition guards
     - violations: []       # STE non-compliance findings
     - optimizations: []    # fixes applied
  4. Output: document overview + extraction plan.

## TURN 1+ — SECTION-BY-SECTION PARSING (REPEAT UNTIL COMPLETE)
For each section of the document:

  STEP 1 — READ
  Read the next section using file-read tool (offset + length).

  STEP 2 — TOKENIZE
  Split text into sentences. For each sentence:
    - Count words (apply P5: ≤20 procedural, ≤25 descriptive).
    - Identify noun clusters (apply P6: ≤3 words).
    - Identify verb tenses (apply P9: only 4 approved).
    - Identify passive voice (apply P3).
    - Identify semicolons (apply P8).
    - Identify gerunds (apply P8).
    - Identify pronouns without antecedent (apply P12).
    - Identify "this" without noun (apply P11).
    - Identify abbreviations not defined (apply P10).

  STEP 3 — LEXICAL CHECK
  For each content word:
    - Check against STE approved vocabulary (P1, P14).
    - Check synonym canonicalization (P2 — use canonical forms table).
    - Check part-of-speech lock (P1 — one POS per word).
    - Check meaning lock (P1 — one meaning per word).

  STEP 4 — EXTRACT STRUCTURAL DATA
  From compliant and corrected text:
    a. ENTITIES → UML CLASSES
       Pattern: [Technical Noun] + description
       Extract: name, attributes, category (1-19)
       Example: "Pressure indicator shows fuel pressure"
         → class PressureIndicator { fuel: Fuel; pressure: Pressure; }
    
    b. RELATIONSHIPS → UML ASSOCIATIONS
       Pattern: Noun + preposition + Noun
       Extract: source, target, type, multiplicity
       Types: association, aggregation, composition, generalization
       Example: "bolt of the flange" → Flange ○-- Bolt (aggregation)
    
    c. PROCEDURES → ORDERED SEQUENCES
       Pattern: Numbered imperative steps
       Extract: step_number, action, object, location
       Example: "Remove the bolt from the flange"
         → step(1, remove, bolt, flange)
    
    d. CONDITIONS → IF-THEN BLOCKS
       Pattern: "If [condition], [action]"
       Extract: condition, action
       Example: "If temperature > 80°C, do paragraph 3"
         → if temp > 80: execute(paragraph_3)
    
    e. SAFETY → PRECONDITION GUARDS
       Pattern: "WARNING: [command]. [reason]"
       Extract: command, reason, target_step
       Example: "WARNING: DO NOT TOUCH. SURFACE IS HOT."
         → @precondition(not touch, "surface is hot")

  STEP 5 — OPTIMIZE
  For each violation found in STEP 2-3:
    - Apply the appropriate STE rewrite rule.
    - Record: original → corrected, rule violated, optimization type.
    - Recount words (before/after).

  STEP 6 — OUTPUT
  Produce the standardized response format:
    ## COMPLIANCE STATUS
    [N violations found | STE-compliant]
    
    ## TECHNICAL OUTPUT
    [Corrected STE text for this section]
    
    ## UML EXTRACTION
    [Mermaid diagram increment for this section]
    
    ## OPTIMIZATIONS
    [Violations → fixes, word count before/after]

  STEP 7 — ADVANCE
  Move to next section. Repeat from STEP 1.
  When no more sections remain, produce final consolidated output.

## FINAL TURN — CONSOLIDATION
  1. Merge all UML extractions into one complete diagram.
  2. Merge all procedures into one ordered execution flow.
  3. Merge all conditions into one decision tree.
  4. Merge all safety constraints into one precondition list.
  5. Summarize: total violations, total fixes, word reduction %.

# UML OUTPUT FORMAT
Use Mermaid syntax for all UML output:

  classDiagram
    class EntityName {
      +attribute: Type
      +method(): ReturnType
    }
    EntityA "1" --> "*" EntityB : relationship_label

  flowchart TD
    A[Start] --> B{Condition?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]

# STATE PERSISTENCE
Between turns, the agent maintains:
  - extraction_state (all arrays from TURN 0)
  - current_section_offset (byte offset in document)
  - cumulative_violation_count
  - cumulative_word_count_original
  - cumulative_word_count_corrected
  - uml_diagram_buffer (accumulated Mermaid syntax)

This state is passed forward each turn until extraction is complete.

================================================================================
END OF EXTRACTION METHODOLOGY
================================================================================
"""

with open("output/ste_extraction_methodology.txt", "w") as f:
    f.write(methodology)

print("Methodology written. Character count:", len(methodology))
print("Token estimate (approx):", len(methodology) // 4)
