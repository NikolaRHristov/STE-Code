
manual_part2 = r"""
═══════════════════════════════════════════════════════════════════════════════
SECTION 3: PAGE-READING PROTOCOL
═══════════════════════════════════════════════════════════════════════════════

3.1 DOCUMENT STATE TRACKING
The agent maintains a persistent state across turns:

  STATE:
    current_page: 1              ← increments after each turn
    total_pages: TBD             ← set on Turn 0 after reading document metadata
    pages_processed: []           ← list of page numbers completed
    extraction_state: {
      skills: [],                 ← extracted skill definitions
      uml_classes: [],            ← UML class diagram candidates
      uml_relationships: [],       ← UML associations between classes
      procedures: [],             ← ordered step sequences
      conditions: [],              ← if-then logic blocks
      safety_guards: [],          ← precondition constraints
      violations: [],              ← STE non-compliance findings
      optimizations: [],           ← fixes applied
      knowledge_fragments: [],    ← new facts learned from this page
    }
    counters: {
      total_violations: 0,
      total_fixes: 0,
      words_original: 0,
      words_corrected: 0,
      skills_extracted: 0,
      uml_elements: 0,
    }

3.2 READING SEQUENCE (EXECUTE ON EVERY TURN)

  STEP A: DETERMINE NEXT PAGE
    - If current_page == 0: This is Turn 0. Read page 1 to get document
      metadata (title, TOC, page count). Set total_pages. Set current_page=1.
    - If current_page > total_pages: This is the final turn. Go to S6 step 6.
    - Otherwise: Read page current_page using file-read tool.

  STEP B: READ THE PAGE
    Use the file-read tool with parameters:
      file: <document_path>
      page: <current_page>
    Read the full page content. Store it in working memory for this turn.

  STEP C: CHECKPOINT
    Before processing, verify:
      - Is this page already in pages_processed? If yes, skip to next page.
      - Is the page blank or a section divider? If yes, record and skip.
      - Does the page contain actual content? If no, skip.

3.3 PAGE CLASSIFICATION
After reading, classify the page type:

  TYPE A — RULE PAGE:
    Contains writing rules (numbered, with examples).
    → Extract: rule number, rule text, STE/non-STE examples.
    → Skill: "Apply Rule X: [constraint]. STE example: [...]. Non-STE: [...]."

  TYPE B — DICTIONARY PAGE:
    Contains word entries (uppercase=approved, lowercase=unapproved).
    → Extract: word, POS, approved meaning, approved forms, alternatives.
    → Skill: "Word X (POS): [meaning]. Forms: [...]. Alternatives: [...]."

  TYPE C — EXAMPLE PAGE:
    Contains worked examples of STE transformations.
    → Extract: non-STE input, STE output, rules applied, transformation passes.
    → Skill: "Transform: [input] → [output]. Rules: [list]. Passes: [count]."

  TYPE D — REFERENCE PAGE:
    Contains TOC, index, copyright, highlights, introduction.
    → Extract: structure, cross-references, change history.
    → Skill: "Reference: [item]. Location: [section]. Cross-ref: [rules]."

  TYPE E — TECHNICAL NAME CATEGORY PAGE:
    Contains category definitions and examples.
    → Extract: category number, category name, example words.
    → Skill: "Technical Noun Category N: [name]. Examples: [...]."

═══════════════════════════════════════════════════════════════════════════════
SECTION 4: SKILL EXTRACTION FRAMEWORK
═══════════════════════════════════════════════════════════════════════════════

4.1 WHAT IS A SKILL?
A skill is a self-contained, actionable knowledge fragment that the agent
can apply to future text. Each skill has this structure:

  SKILL DEFINITION FORMAT:
    skill_id: S[page]_[sequential]
    skill_type: rule | dictionary | transformation | reference | category
    trigger: "When text contains [pattern], apply [action]."
    content: [The actual rule, word definition, or transformation]
    examples: [{ input: "...", output: "..." }]
    source: "Page [N], Section [X.Y]"

4.2 SKILL EXTRACTION PATTERNS

  PATTERN 1 — RULE EXTRACTION (from TYPE A pages)
    trigger: "When writing [context], [constraint]."
    content: "STE Rule [N.M]: [rule text]"
    examples: from the page's STE/non-STE pairs
    → Example skill:
      skill_id: S15_001
      trigger: "When writing a noun cluster, limit to 3 words."
      content: "Rule 2.1: A noun cluster must not contain more than 3 words."
      examples: [
        { input: "engine fuel pump pressure indicator",
          output: "the pressure indicator of the engine fuel pump" }
      ]
      source: "Page 15, Section 2"

  PATTERN 2 — WORD EXTRACTION (from TYPE B pages)
    trigger: "When using the word [WORD], use only as [POS] meaning [sense]."
    content: "[WORD] ([POS]): [approved meaning]. Forms: [list]."
    → Example skill:
      skill_id: S42_005
      trigger: "When using REMOVE, use only as a verb meaning 'take away'."
      content: "REMOVE (v): to take away from a location.
                Forms: REMOVES, REMOVED, REMOVED."
      source: "Page 42, Section 2 (Dictionary)"

  PATTERN 3 — TRANSFORMATION EXTRACTION (from TYPE C pages)
    trigger: "When text contains [non-STE pattern], rewrite to [STE form]."
    content: "[transformation description]. Apply rules: [list]."
    → Example skill:
      skill_id: S78_003
      trigger: "When text uses passive voice in a procedure, rewrite to active."
      content: "Passive→Active: 'The bolt should be removed' → 'Remove the bolt.'
                Apply rules: 3.6, 3.2. Passes: 5."
      source: "Page 78, Example Section"

  PATTERN 4 — POLYSEMY RESOLUTION (from TYPE B pages)
    trigger: "When [WORD] is used in the sense of [unapproved sense],
              use [approved alternative] instead."
    → Example skill:
      skill_id: S43_002
      trigger: "When FOLLOW means 'obey', use OBEY instead."
      content: "FOLLOW means 'come after' only. For 'obey', use OBEY."
      source: "Page 43, Dictionary entry FOLLOW"

  PATTERN 5 — SYNONYM ELIMINATION (from TYPE B pages)
    trigger: "When tempted to use [synonym], use [canonical form] instead."
    → Example skill:
      skill_id: S44_007
      trigger: "When tempted to use 'ensure', use 'MAKE SURE' instead."
      content: "Canonical: MAKE SURE. Not: ensure, verify, ascertain, confirm."
      source: "Page 44, Dictionary entry ENSURE (unapproved)"

4.3 SKILL ACCUMULATION
After each page, append all extracted skills to extraction_state.skills.
The growing skill list becomes the agent's executable knowledge base.
On the final turn, output all skills as a consolidated skill file.

═══════════════════════════════════════════════════════════════════════════════
SECTION 5: UML EXTRACTION FRAMEWORK
═══════════════════════════════════════════════════════════════════════════════

5.1 EXTRACTION TARGETS

  A. CLASSES (from nouns and technical nouns):
    Pattern: [Technical Noun] + description or attributes
    → class ClassName { +attribute: Type }
    Example: "The pressure indicator shows the fuel pressure"
      → class PressureIndicator { +fuel: Fuel; +pressure: Pressure }

  B. ASSOCIATIONS (from prepositional relationships):
    Pattern: Noun + preposition + Noun
    → ClassA "mult" --> "mult" ClassB : label
    Example: "bolt of the flange"
      → Flange "1" o-- "*" Bolt : contains

  C. PROCEDURES (from numbered steps):
    Pattern: Numbered imperative + object + location
    → step(N, action, object, location)
    Example: "1. Remove the bolt from the flange"
      → flowchart: A[Remove bolt from flange]

  D. CONDITIONS (from if-then constructions):
    Pattern: "If [condition], [action]"
    → {condition} -->|Yes| [action]
    Example: "If temperature > 80°C, do paragraph 3"
      → {temp > 80°C?} -->|Yes| [Execute paragraph 3]

  E. SAFETY GUARDS (from warnings/cautions):
    Pattern: "WARNING: [command]. [reason]."
    → note: [reason] before [target_step]
    Example: "WARNING: DO NOT TOUCH. SURFACE IS HOT."
      → note right of A: ⚠ SURFACE IS HOT

5.2 MERMAID OUTPUT FORMAT
Use Mermaid syntax for all UML. Accumulate across turns. On the final
turn, output one complete diagram.

  classDiagram
    class ClassName {
      +attr: Type
      +method(): Type
    }
    ClassA "1" --> "*" ClassB : label

  flowchart TD
    A[Start] --> B{Condition?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]

5.3 UML ACCUMULATION BUFFER
After each page, append new UML elements to extraction_state.uml_classes
and extraction_state.uml_relationships. On the final turn, merge all
elements into one diagram. Remove duplicates. Resolve naming conflicts.
"""

with open("output/ste_self_reading_manual.txt", "a") as f:
    f.write(manual_part2)

print("Manual part 2 appended. Chars:", len(manual_part2))
