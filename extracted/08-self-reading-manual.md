# STE Self-Reading Manual (SSRM v1.0) — Architecture and Recursive Loop

> Extracted and restructured from Perplexity conversation.
> The self-referencing recursive extraction system for local LLM agents.

---

## Overview

The STE Self-Reading Manual (SSRM v1.0) is a **self-referencing recursive extraction system** that a local LLM can use to read the ASD-STE100 specification (or any technical document) page by page, extract skills and UML on each turn, and continue recursively until all pages are processed — all while enforcing STE compliance on its own output.

The manual serves as the **operating system for the local agent** — the agent re-reads it on every turn to determine its next action.

---

## Five-File System

| File | Tokens | Purpose |
|------|--------|---------|
| `ste_distilled_system_prompt.txt` | ~1,240 | 14 core principles, synonym table, anti-patterns. Insert as system prompt. |
| `ste_self_reading_manual.txt` | ~6,897 | The recursive extraction manual. Insert as first user message. |
| `ste_extraction_methodology.txt` | ~1,401 | Turn-by-turn protocol details. Second user message. |
| `ste_example_turn.txt` | ~503 | Worked example showing one extraction turn. Few-shot prompt. |
| `ste_deployment_guide.txt` | ~1,876 | Deployment instructions for Ollama, LM Studio, Python + llama.cpp. |

**Total system overhead: ~11,917 tokens**

---

## Manual Structure (8 Sections)

### Section 0 — How to Use This Manual

Tells the agent how to use the manual itself — establishing the **recursive loop**:

```
read S3 (page protocol) → read page → read S4 (skill extraction) → extract
→ read S5 (UML extraction) → extract → read S6 (self-questioning)
→ answer 13 questions → read S7 (output format) → output → loop back to S3
```

### Section 1 — Core STE Principles

Contains the 14 distilled STE principles and the canonical synonym table — the rules the agent enforces on all text it produces and analyzes.

### Section 2 — Knowledge Base

The distilled knowledge base from the full specification:
- All 53 rules organized by section
- The 19 technical noun categories
- Polysemy resolution table
- The 6-pass transformation pipeline
- Specification evolution history from Issue 1 to Issue 9

This is the compact representation of the entire ASD-STE100 that fits in context alongside the manual.

### Section 3 — Page-Reading Protocol

Document state tracking, reading sequence, and page classification:

**State tracking:**
```
current_page: 1
total_pages: TBD
pages_processed: []
extraction_state: {
    skills: [],
    uml_classes: [],
    uml_relationships: [],
    procedures: [],
    conditions: [],
    safety_guards: [],
    violations: [],
    optimizations: [],
    knowledge_fragments: []
}
counters: {
    total_violations, total_fixes,
    words_original, words_corrected,
    skills_extracted, uml_elements
}
```

**5 page types for classification:**

| Type | Content | Action |
|------|---------|--------|
| A — Rule Page | Writing rules (numbered, with examples) | Extract rule number, text, STE/non-STE examples |
| B — Dictionary Page | Word entries (uppercase=approved, lowercase=unapproved) | Extract word, POS, meaning, forms, alternatives |
| C — Example Page | Worked examples of STE transformations | Extract non-STE input, STE output, rules applied |
| D — Reference Page | TOC, index, copyright, highlights | Extract structure, cross-references, change history |
| E — Category Page | Category definitions and examples | Extract category number, name, example words |

### Section 4 — Skill Extraction Framework

5 patterns for extracting skills — each skill has a structured format with ID, trigger, content, examples, and source reference:

1. **Pattern 1 — Rule Extraction** (from Type A pages): "When writing [context], [constraint]"
2. **Pattern 2 — Word Extraction** (from Type B pages): "When using [WORD], use only as [POS] meaning [sense]"
3. **Pattern 3 — Transformation Extraction** (from Type C pages): "When text contains [non-STE pattern], rewrite to [STE form]"
4. **Pattern 4 — Polysemy Resolution** (from Type B pages): "When [WORD] is used in the sense of [unapproved sense], use [approved alternative] instead"
5. **Pattern 5 — Synonym Elimination** (from Type B pages): "When tempted to use [synonym], use [canonical form] instead"

### Section 5 — UML Extraction Framework

Patterns for extracting:
- **Classes** — from nouns: `[Technical Noun] + description` → `class ClassName { +attribute: Type }`
- **Associations** — from prepositional phrases: `Noun + preposition + Noun` → `ClassA "mult" --> "mult" ClassB : label`
- **Procedures** — from numbered steps: `Numbered imperative + object + location` → flowchart nodes
- **Conditions** — from if-then: `"If [condition], [action]"` → decision nodes
- **Safety Guards** — from warnings: `"WARNING: [command]. [reason]"` → precondition guards

All UML is accumulated in **Mermaid syntax** across turns.

### Section 6 — Recursive Questioning Protocol

13 questions the agent asks itself on every turn, in order:

| Q# | Question | Action |
|----|----------|--------|
| Q1 | "Have I read page current_page?" | If NO: Read it now. If YES: Continue to Q2 |
| Q2 | "What type of page is this?" | Classify per S3.3 → branch to Q3-Q7 |
| Q3 | (TYPE A — Rule pages): "What rules, examples, entities, relationships, procedures, conditions, safety, violations?" | Extract to skills + UML |
| Q4 | (TYPE B — Dictionary): "What words, POS, meanings, polysemy, alternatives, UML?" | Extract to skills + UML |
| Q5 | (TYPE C — Example): "What is the non-STE input, STE output, rules, passes, word count, generalizable skill?" | Extract and optimize |
| Q6 | (TYPE D — Reference): "What structural info, cross-references, change history, total pages?" | Record metadata |
| Q7 | (TYPE E — Category): "What category number, name, example words, UML entities?" | Extract to skills + UML |
| Q8 | "Have I extracted all skills from this page?" | If NO: Re-read page. If YES: Continue |
| Q9 | "Have I extracted all UML elements?" | If NO: Re-read for nouns, relationships, procedures |
| Q10 | "Have I recorded all violations and optimizations?" | If NO: Scan for STE non-compliance |
| Q11 | "Have I updated all counters?" | Update cumulative state |
| Q12 | "Is current_page the last page?" | If NO: Increment, go to Q1 (RECURSIVE LOOP). If YES: Go to Q13 |
| Q13 | "Am I ready to produce the final consolidated output?" | If YES: Go to S7, FINAL OUTPUT FORMAT |

**Recursive self-correction**: If a previously extracted skill contradicts new information, the agent flags it, re-reads the earlier page, determines the correct interpretation, updates the skill, and records the correction.

### Section 8 — Context Window Management

**Persistent (keep in context):**
- This manual (SSRM) — always in context
- `extraction_state` — the growing arrays of skills, UML, violations
- `counters` — the running totals
- `current_page` and `total_pages`

**Ephemeral (discard after each turn):**
- The raw page text read during the turn (free the context)
- Intermediate analysis that has been extracted to skills or UML
- Do not keep raw pages in context. Only keep extracted knowledge.

**Checkpoint protocol (for large documents, every 20 pages):**
1. Write `extraction_state` to a checkpoint file (JSON)
2. Clear the context window
3. Reload this manual + system prompt + checkpoint file
4. Continue from `current_page`

**Token budget:**
- Manual: ~7,000 tokens
- System prompt: ~1,200 tokens
- Per-turn page text: ~2,000–4,000 tokens
- Per-turn output: ~500–1,000 tokens
- Estimated capacity: 100+ pages in a 128K context window

---

## How the Recursive Loop Works

1. The agent receives the manual as its first instruction.
2. **Turn 0**: Reads page 1 of the target document, extracts metadata (title, page count), initializes extraction state.
3. **Each subsequent turn**: Reads one page, classifies it, asks itself the 13 questions from Section 6, extracts skills (S4) and UML elements (S5), records violations and optimizations, outputs in the standardized format (S7), increments the page counter, and loops back.
4. The agent **self-references the manual** on every turn — it re-reads S6 to know which questions to ask, re-reads S3 to know how to read the next page, and re-reads S7 to know how to format output.
5. **Final turn**: Produces consolidated output.

---

## What the Agent Produces (Final Consolidated Output)

After processing all pages, the agent produces:

### 1. Skill Library

- All 53 rules as executable skills with triggers and examples
- All ~875 dictionary words as typed definitions
- All polysemy resolutions as constraint skills
- All synonym eliminations as canonical form skills
- All 19 technical noun categories as classification skills
- All transformation patterns as rewrite skills

### 2. UML Class Diagram

- Every technical noun as a class
- Every prepositional relationship as an association
- Every attribute mentioned as a class property
- Every system/component as a class with methods
- All in renderable Mermaid syntax

### 3. UML Flowchart

- Every procedural step as a node
- Every condition as a decision node
- Every safety instruction as a precondition guard
- Complete execution flow from start to end

### 4. Compliance Report

- Every STE violation found in the source document
- Every fix applied with before/after text
- Word count reduction percentage
- Overall compliance certificate

### 5. Reusable Knowledge

- The skill library can be saved and loaded into future sessions
- The UML diagrams can be rendered in any Mermaid viewer
- The compliance report serves as documentation
- The entire extraction state can be checkpointed and resumed

---

## Providing the Full Conversation as Context

The deployment guide (Option D) explains how to export the entire conversation as a markdown file and inject it as additional context before the manual. This gives the local model both the distilled rules from the system prompt AND the detailed analysis from the conversation — all 53 rules, the dictionary architecture, the transformation grammar, the impact on code/MT/NLP, and the evolution history.

The conversation adds approximately 15,000–20,000 tokens of rich extracted knowledge on top of the ~11,917-token system overhead, still leaving 90,000+ tokens for document pages and output in a 128K context window.

---

## References

- https://www.asd-ste100.org/
- https://www.asd-ste100.org/about.html
- https://www.youtube.com/watch?v=ffF-V7xQL68
