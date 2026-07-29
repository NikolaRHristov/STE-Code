
deployment_guide = """================================================================================
LOCAL LLM DEPLOYMENT GUIDE FOR STE SELF-READING SYSTEM
================================================================================

This guide explains how to deploy the complete STE extraction system on a
local LLM using the files generated in this conversation.

--------------------------------------------------------------------------------
PREREQUISITE FILES (all generated, available for download)
--------------------------------------------------------------------------------
1. ste_distilled_system_prompt.txt     (~1,240 tokens)
   The STE rule set. Insert as system prompt.
2. ste_self_reading_manual.txt          (~6,897 tokens)
   The recursive extraction manual. Insert as first user message.
3. ste_extraction_methodology.txt       (~1,401 tokens)
   Turn-by-turn protocol. Insert as second user message.
4. ste_example_turn.txt                  (~503 tokens)
   Worked example. Insert as third user message (few-shot).

Total context budget for system: ~10,041 tokens
Remaining context for document pages + output: ~117,959 tokens (128K window)

--------------------------------------------------------------------------------
DEPLOYMENT OPTIONS
--------------------------------------------------------------------------------

OPTION A: OLLAMA (recommended for local inference)
  1. Create a Modelfile:

     FROM llama3.1:8b-instruct-q8_0
     SYSTEM (paste contents of ste_distilled_system_prompt.txt)
     PARAMETER temperature 0.1
     PARAMETER num_ctx 131072
     PARAMETER repeat_penalty 1.1
     PARAMETER top_p 0.9

  2. Build the model:
     ollama create ste-agent -f Modelfile

  3. Start the extraction:
     ollama run ste-agent (paste contents of ste_self_reading_manual.txt)
     Then provide the document path and let it run recursively.

OPTION B: LM STUDIO (GUI-based)
  1. Load a model with 128K context (e.g., Qwen2.5-14B, Llama 3.1 8B).
  2. Set system prompt to contents of ste_distilled_system_prompt.txt.
  3. Paste ste_self_reading_manual.txt as first user message.
  4. Paste ste_extraction_methodology.txt as second message.
  5. Paste ste_example_turn.txt as third message.
  6. Provide the document file path. Instruct: Read page 1.
  7. Continue the conversation, prompting "continue" after each turn.

OPTION C: PYTHON + LLAMA.CPP (programmatic, for automation)

  from llama_cpp import Llama

  llm = Llama(model_path="model.gguf", n_ctx=131072)

  system_prompt = open("ste_distilled_system_prompt.txt").read()
  manual = open("ste_self_reading_manual.txt").read()
  methodology = open("ste_extraction_methodology.txt").read()
  example = open("ste_example_turn.txt").read()

  messages = [
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": manual},
      {"role": "assistant", "content": "Manual loaded. I am ready to begin extraction."},
      {"role": "user", "content": methodology},
      {"role": "assistant", "content": "Methodology loaded. Awaiting document."},
      {"role": "user", "content": example},
      {"role": "assistant", "content": "Example processed. Awaiting document."},
      {"role": "user", "content": "Document path here. Read page 1."},
  ]

  # Recursive loop
  while True:
      response = llm.create_chat_completion(messages=messages, temperature=0.1)
      reply = response["choices"][0]["message"]["content"]
      messages.append({"role": "assistant", "content": reply})

      if "FINAL CONSOLIDATED OUTPUT" in reply:
          break

      messages.append({"role": "user", "content": "continue"})

OPTION D: PROVIDING THE FULL CONVERSATION
  You can also export this entire conversation (Parts 1-5) as a markdown file
  and provide it alongside the manual. This gives the local model the full
  extracted knowledge from the ASD-STE100 specification as context.

  To do this:
  1. Save this conversation as conversation.md.
  2. Add it to the context as an additional user message before the manual.
  3. The model now has both the distilled rules AND the detailed analysis.

--------------------------------------------------------------------------------
RECURSIVE EXTRACTION FLOW
--------------------------------------------------------------------------------

Turn 0:  Agent reads page 1, extracts metadata, sets total_pages
Turn 1:  Agent reads page 2, classifies page type, extracts skills + UML
Turn 2:  Agent reads page 3, classifies, extracts, outputs
...
Turn N:  Agent reads last page, extracts, outputs FINAL CONSOLIDATED OUTPUT

Each turn, the agent:
  1. Reads the next page (file-read tool or context injection)
  2. Asks itself 13 questions (S6 recursive questioning protocol)
  3. Extracts skills (S4 framework)
  4. Extracts UML elements (S5 framework)
  5. Records violations and optimizations
  6. Outputs in the standardized format (S7)
  7. Increments current_page
  8. Loops back to step 1

The agent self-references the manual on every turn to know:
  - What to extract (S4 skills, S5 UML)
  - What to ask itself (S6 questions)
  - How to output (S7 format)
  - How to manage context (S8 checkpointing)

--------------------------------------------------------------------------------
EXPECTED OUTPUTS AFTER COMPLETE EXTRACTION
--------------------------------------------------------------------------------
After processing all pages, the agent produces:

1. SKILL LIBRARY
   - All 53 rules as executable skills with triggers and examples
   - All ~875 dictionary words as typed definitions
   - All polysemy resolutions as constraint skills
   - All synonym eliminations as canonical form skills
   - All 19 technical noun categories as classification skills
   - All transformation patterns as rewrite skills

2. UML CLASS DIAGRAM
   - Every technical noun as a class
   - Every prepositional relationship as an association
   - Every attribute mentioned as a class property
   - Every system/component as a class with methods

3. UML FLOWCHART
   - Every procedural step as a node
   - Every condition as a decision node
   - Every safety instruction as a precondition guard
   - Complete execution flow from start to end

4. COMPLIANCE REPORT
   - Every STE violation found in the source document
   - Every fix applied with before/after text
   - Word count reduction percentage
   - Overall compliance certificate

5. REUSABLE KNOWLEDGE
   - The skill library can be saved and loaded into future sessions
   - The UML diagrams can be rendered in any Mermaid viewer
   - The compliance report serves as documentation
   - The entire extraction state can be checkpointed and resumed

--------------------------------------------------------------------------------
SYSTEM PROMPT + MANUAL COMBINED TOKEN BUDGET
--------------------------------------------------------------------------------
  ste_distilled_system_prompt.txt:     ~1,240 tokens
  ste_self_reading_manual.txt:          ~6,897 tokens
  ste_extraction_methodology.txt:       ~1,401 tokens
  ste_example_turn.txt:                  ~503 tokens
  ---------------------------------------------------------------
  Total system overhead:               ~10,041 tokens

  Available for document + output:     ~117,959 tokens (128K context)
  Estimated pages processable:         50-100+ (with checkpointing: unlimited)

================================================================================
END OF DEPLOYMENT GUIDE
================================================================================
"""

with open("output/ste_deployment_guide.txt", "w") as f:
    f.write(deployment_guide)

import os
size = os.path.getsize("output/ste_deployment_guide.txt")
with open("output/ste_deployment_guide.txt", "r") as f:
    chars = len(f.read())
print(f"Deployment guide written. {size:,} bytes, ~{chars//4:,} tokens")

print("\n=== COMPLETE FILE SET ===")
files = [
    ("ste_distilled_system_prompt.txt", "System prompt (STE rules)"),
    ("ste_self_reading_manual.txt", "Self-reading manual (recursive protocol)"),
    ("ste_extraction_methodology.txt", "Extraction methodology (turn-by-turn)"),
    ("ste_example_turn.txt", "Worked example (few-shot)"),
    ("ste_deployment_guide.txt", "Deployment guide (Ollama/LM Studio/Python)"),
]
total_tokens = 0
for fname, desc in files:
    with open(f"output/{fname}", "r") as f:
        c = len(f.read())
    t = c // 4
    total_tokens += t
    print(f"  {fname:42s} ~{t:>5,} tokens  ({desc})")
print(f"  {'TOTAL':42s} ~{total_tokens:>5,} tokens")
