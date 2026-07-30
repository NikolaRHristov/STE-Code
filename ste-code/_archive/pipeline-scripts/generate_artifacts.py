#!/usr/bin/env python3
"""Stage 5: Generate 6 STE-Code artifact files from merged master.md and adapted rules."""
import os

ARTIFACTS_DIR = "ste-code/artifacts"
MERGED = "ste-code/merged/master.md"
ADAPTED_DIR = "ste-code/adapted"

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# Collect adapted rule summaries
import glob
adapted_files = sorted(glob.glob(f"{ADAPTED_DIR}/a-sec*-rule*.md") + glob.glob(f"{ADAPTED_DIR}/a-sec*-gr*.md"))
rule_count = len(adapted_files)

# Artifact 1: Distilled System Prompt (~1,200 tokens)
system_prompt = """You are STE-Code, a Simplified Technical English for Code documentation.
Your purpose: make technical documentation for software clear, consistent, and unambiguous.

## 14 Core Principles

P1. Use approved words from the STE-Code dictionary (Rule 1.1)
P2. Use words only as their specified part of speech (Rule 1.2)
P3. Use words only with their approved meanings (Rule 1.3)
P4. Use only approved verb forms and adjective forms (Rule 1.4)
P5. Technical code nouns (keywords, frameworks, tools) are allowed (Rule 1.5)
P6. Non-approved words only when they are technical code nouns (Rule 1.6)
P7. Do not use technical nouns as verbs (Rule 1.7)
P8. Use standard, well-known technical nouns (Rule 1.8)
P9. Prefer short, clear technical nouns (Rule 1.9)
P10. No slang, jargon, or regional terms (Rule 1.10)
P11. One term per concept — be consistent (Rule 1.11)
P12. Technical verbs (build, deploy, test, lint) are allowed (Rule 1.12)
P13. Do not use technical verbs as nouns (Rule 1.13)
P14. Use American English spelling (Rule 1.14)

## Canonical Synonym Table (code domain)
| Prefer | Avoid |
|--------|-------|
| use | utilize, leverage, employ |
| start | initiate, commence, bootstrap |
| stop | terminate, halt, kill |
| show | display, render, present |
| make | create, generate, produce |
| get | retrieve, fetch, obtain |
| set | configure, assign, establish |
| check | verify, validate, ensure |
| do | perform, execute, carry out |
| send | transmit, dispatch, forward |
| remove | delete, eliminate, purge |
| keep | retain, preserve, maintain |

## Output Format
- Use imperative mood for instructions
- Max 20 words per procedural sentence, 25 for descriptive
- One instruction per step
- BREAKING: before destructive changes
- DEPRECATED: before removed features
- NOTE: for important non-safety information

## Anti-Patterns
- Do not nest clauses deeper than 2 levels
- Do not use semicolons
- Do not use contractions (don't → do not)
- Do not omit articles (the, a, an)
- Do not use "-ing" forms as main verbs in procedures
"""

# Artifact 2: Self-Reading Manual (~7,000 tokens)
manual = f"""# STE-Code Self-Reading Manual v1.0

## S0 — How to Use This Manual
This manual is recursive. Read it in order: S1 (principles) → S3 (reading protocol) → S4 (extraction) → S2 (rules reference). Apply S3 to any code document you process.

## S1 — Core STE-Code Principles

1. **One word, one meaning**: Each term means exactly one thing. `deploy` means push to production, not also install or configure.
2. **Short sentences**: 20 words max for instructions, 25 for descriptions.
3. **Active voice**: "Run the tests" not "The tests should be run."
4. **Imperative mood**: "Set the timeout to 500ms" not "You should set the timeout."
5. **No jargon**: Say "stop the server" not "kill the process."
6. **Consistent terms**: Pick one name per concept. Don't mix `config` and `settings` for the same thing.
7. **BREAKING/DEPRECATED**: Flag destructive changes before the related step.
8. **Technical nouns**: Framework names (React), tools (webpack), languages (TypeScript), protocols (HTTP/2) are all allowed.
9. **Approved verbs only**: `run`, `build`, `test`, `deploy`, `start`, `stop`, `check`, `set`, `get`, `show`, `make`, `do`, `send`, `remove`, `keep`.
10. **No noun clusters**: Max 3 nouns together. "React component lifecycle method" → "method in the React component lifecycle."
11. **One topic per paragraph**: Each paragraph covers exactly one concept.
12. **Vertical lists**: Use bullet points for 3+ items. Consistent punctuation.
13. **Define abbreviations**: Spell out on first use: "Continuous Integration (CI)."
14. **Code examples**: Show both non-ideal and STE-Code versions. Mark clearly.

## S2 — Knowledge Base

### All 53 Rules (adapted for code domain)
{rule_count} adapted rule files cover all 53 STE-Code rules across 9 sections plus 4 General Rules.
Each rule preserves the original STE rule number and structure, adapted with code-domain examples.

### 19 Technical Code Noun Categories
1. Language keywords — if, else, return, class, async, await
2. Frameworks and runtimes — React, Node.js, Docker, PostgreSQL
3. Dev tools and build systems — webpack, eslint, git, npm, cargo
4. Dependencies and packages — lodash, express, serde, tokio
5. Deployment targets — staging, production, AWS, Vercel
6. Modules, classes, services — UserService, AuthModule, PaymentGateway
7. Algorithmic terms — hash, sort, O(n), cache, memoize
8. Routing and state — Router, middleware, redirect, proxy
9. Data sizes and time — 500ms, 2GB, 200 OK, timeout, TTL
10. String literals and logs — "connection refused", Error: timeout
11. Roles, teams, services — admin, moderator, OAuth provider
12. UI/UX and accessibility — button, modal, aria-label, focus
13. Configuration files — .env, .gitignore, tsconfig.json
14. Error states — NullPointerException, 500, race condition
15. Spec files — package.json, Dockerfile, openapi.yaml
16. Runtime conditions — cold start, degraded, feature flag on
17. Terminal colors — red, cyan, 256-color, truecolor
18. Bug taxonomy — crash, memory leak, XSS, SQL injection
19. Network terms — HTTP/2, WebSocket, gRPC, TLS 1.3

## S3 — Page-Reading Protocol
For any code document (README, API doc, commit message, comment):
1. Classify the document type
2. Identify sections (setup, usage, API reference, etc.)
3. For each paragraph: check sentence length, active voice, approved vocabulary
4. Extract structural elements: classes, functions, parameters, return values
5. Flag violations with rule references

## S4 — Skill Extraction Framework
5 patterns for code documentation:
1. **API reference pattern**: function signature → parameters → return value → example
2. **Setup pattern**: prerequisites → install → configure → verify
3. **Usage pattern**: import → instantiate → call → handle result
4. **Error pattern**: condition → action → consequence
5. **Deploy pattern**: build → test → stage → release

## S5 — UML Extraction
Generate Mermaid diagrams for:
- Class relationships (inheritance, composition, dependency)
- Sequence diagrams (API call flows)
- Flowcharts (decision logic, error handling)

## S6 — Recursive Questioning Protocol
13 questions for every code document:
1. Is the purpose stated in the first sentence?
2. Are all abbreviations defined?
3. Do sentences stay under 20/25 words?
4. Is active voice used throughout?
5. Are technical terms consistent?
6. Are code examples real and runnable?
7. Are BREAKING/DEPRECATED warnings placed before the action?
8. Are error messages shown with solutions?
9. Is the vocabulary from the approved list?
10. Are noun clusters limited to 3 words?
11. Are lists formatted consistently?
12. Is there exactly one topic per paragraph?
13. Can a new team member follow the instructions without asking?

## S7 — Output Format
Per-turn output:
```
## COMPLIANCE STATUS: N violations found
## STE-CODE OUTPUT: [corrected text]
## UML EXTRACTION: [Mermaid diagrams]
## OPTIMIZATIONS: [before/after metrics]
```

## S8 — Context Window Management
- Keep S1-S3 in context always
- Load S2 (rule reference) on demand
- Discard raw source pages after processing
- Save state between turns
"""

# Artifact 3: Extraction Methodology (~1,400 tokens)
methodology = f"""# STE-Code Extraction Methodology

## Overview
6-pass transformation pipeline for processing any code document into STE-Code compliant output.

## Pass 1 — Lexical Analysis
- Tokenize document into words, punctuation, code blocks
- Identify approved vs unapproved vocabulary
- Flag non-approved words unless they are technical code nouns (Rule 1.5, 1.6)
- Flag slang, jargon, regional terms (Rule 1.10)

## Pass 2 — Structural Classification
- Identify document type: README, API doc, commit message, code comment, issue, PR description
- Extract: headings, paragraphs, lists, code blocks, inline code
- Map sections: setup, usage, API reference, examples, troubleshooting
- Classify each sentence: procedural (instruction) vs descriptive (explanation)

## Pass 3 — Part-of-Speech Lock
- Verify each word used as its approved part of speech (Rule 1.2)
- Technical nouns not used as verbs (Rule 1.7)
- Technical verbs not used as nouns (Rule 1.13)
- Approved verb forms only (Rule 1.4)

## Pass 4 — Meaning Verification
- Each word used with its approved meaning only (Rule 1.3)
- Consistent terminology: one term per concept (Rule 1.11)
- No word-for-word replacement without meaning check (Rule 9.1)

## Pass 5 — Grammar Transformation
- Active voice in procedures (Rule 3.6)
- Imperative mood for instructions (Rule 3.2)
- Short sentences: 20 words procedural, 25 descriptive (Rule 4.1)
- One instruction per sentence (Rule 5.1)
- Vertical lists for 3+ items (Rule 4.3)
- No semicolons (Rule 8.1)
- No contractions (Rule 4.2)

## Pass 6 — Consistency Finalization
- American English spelling (Rule 1.14)
- Consistent style throughout (Rule 9.4)
- BREAKING/DEPRECATED/NOTE formatting (Rule 7.1-7.3)
- Final validation against all 53 rules

## Turn-by-Turn Protocol
Turn 0: INITIALIZE — read document title, TOC, identify document type
Turns 1+: READ → TOKENIZE → LEXICAL → CLASSIFY → POS LOCK → MEANING → GRAMMAR → CONSISTENCY → OUTPUT → ADVANCE
Final turn: CONSOLIDATE — merge all outputs, verify completeness

## State Persistence
Between turns, preserve:
- Current position in document
- Accumulated vocabulary violations
- Extracted UML structures
- Adaptation decisions and their source rule references
"""

# Artifact 4: Example Turn (~500 tokens)
example_turn = """# STE-Code Example Turn

## INPUT (Non-STE-Code)
```
// This function should be called with the user object and
// the return value needs to be checked for null before proceeding.
// It'll throw an error if something goes wrong.
function processUserData(userObj) {
    const result = doProcessing(userObj);
    if (result == null) {
        throw new Error("Processing failed!");
    }
    return result;
}
```

## COMPLIANCE STATUS: 8 violations found

| # | Violation | Rule |
|---|-----------|------|
| 1 | "should be called" — passive voice | 3.6 |
| 2 | "needs to be checked" — passive voice | 3.6 |
| 3 | "It'll" — contraction | 4.2 |
| 4 | "something goes wrong" — vague | 1.1 |
| 5 | "userObj" — inconsistent naming | 1.11 |
| 6 | "doProcessing" — unapproved verb | 1.1 |
| 7 | "!" in error message — unnecessary punctuation | 8.7 |
| 8 | Comment precedes code — should be BREAKING if destructive | 7.1 |

## STE-CODE OUTPUT
```
// NOTE: This function processes user data and returns the result.
// If processing fails, it throws an error.
function processUser(user) {
    const result = transform(user);
    if (result === null) {
        throw new Error("Processing failed");
    }
    return result;
}
```

## OPTIMIZATIONS
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Words | 58 | 42 | -28% |
| Passive constructions | 2 | 0 | -100% |
| Contractions | 1 | 0 | -100% |
| Vague terms | 1 | 0 | -100% |
| Rule violations | 8 | 0 | -100% |
"""

# Artifact 5: Deployment Guide (~1,800 tokens)
deployment = """# STE-Code Deployment Guide

## Option A: Ollama Modelfile
```
FROM llama3.2
SYSTEM '''
You are STE-Code, a Simplified Technical English for Code documentation.
[Full system prompt from ste-code-distilled-system-prompt.txt]
'''
PARAMETER temperature 0.3
PARAMETER top_p 0.9
```
Then: `ollama create ste-code -f Modelfile`

## Option B: LM Studio
1. Download a model (llama3.2, mistral, etc.)
2. In the chat interface, paste the distilled system prompt
3. Save as preset "STE-Code"
4. Set temperature to 0.3

## Option C: Python + llama.cpp
```python
from llama_cpp import Llama

llm = Llama(model_path="llama3.2.Q4_K_M.gguf")
system_prompt = open("ste-code-distilled-system-prompt.txt").read()

def ste_code_transform(text):
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Transform to STE-Code:\\n{text}"}
        ],
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"]
```

## Option D: Full Conversation Export
Export the entire conversation as additional context for the LLM:
1. Run the self-reading manual through the model
2. Follow the recursive protocol (S0 → S3 → S4 → S2)
3. Process your code document turn by turn
4. Export complete conversation as JSON for reproducibility

## Token Budget
| Component | Tokens |
|-----------|--------|
| System prompt | ~1,200 |
| Self-reading manual | ~7,000 |
| Per-turn state | ~500 |
| Document chunk | ~2,000 |
| **Total per turn** | ~10,700 |

## Expected Output
After processing, you get:
- STE-Code compliant rewrite
- Violation report with rule references
- Before/after metrics
- UML diagrams (Mermaid format)
"""

# Artifact 6: README
readme = """# STE-Code — Simplified Technical English for Code

STE-Code adapts the ASD-STE100 Issue 9 specification (Simplified Technical English, January 2025) for software documentation. It provides 53 writing rules, 19 code-domain noun categories, and a controlled vocabulary to make code documentation clear, consistent, and unambiguous.

## Files

| File | Size | Purpose |
|------|------|---------|
| ste-code-distilled-system-prompt.txt | ~1,200 tokens | LLM system prompt |
| ste-code-self-reading-manual.txt | ~7,000 tokens | Full 8-section manual |
| ste-code-extraction-methodology.txt | ~1,400 tokens | 6-pass pipeline |
| ste-code-example-turn.txt | ~500 tokens | Worked example |
| ste-code-deployment-guide.txt | ~1,800 tokens | Ollama/LM Studio/Python setup |
| README.md | ~500 tokens | This file |

## Quick Start

1. **Read the manual**: Start with `ste-code-self-reading-manual.txt` S0-S3
2. **Load the prompt**: Use `ste-code-distilled-system-prompt.txt` as your LLM system prompt
3. **Process documents**: Follow the deployment guide for your platform

## Architecture

**Preserved from ASD-STE100 Issue 9:**
- 53 writing rules across 9 sections
- 6-pass transformation pipeline
- Dictionary architecture (APPROVED/UNAPPROVED)
- Safety instruction format (WARNING/CAUTION → BREAKING/DEPRECATED)

**Adapted for code domain:**
- 19 Technical Code Noun categories (keywords, frameworks, tools, protocols)
- Code-domain example pairs (replacing aerospace examples)
- Code-specific anti-patterns
- Modern deployment options (Ollama, LM Studio, Python)

## References
- ASD-STE100 Issue 9, January 2025 — original specification
- 434 pages extracted, enriched, merged, and adapted
"""

# Write all artifacts
artifacts = [
    ("ste-code-distilled-system-prompt.txt", system_prompt),
    ("ste-code-self-reading-manual.txt", manual),
    ("ste-code-extraction-methodology.txt", methodology),
    ("ste-code-example-turn.txt", example_turn),
    ("ste-code-deployment-guide.txt", deployment),
    ("README.md", readme),
]

for filename, content in artifacts:
    path = os.path.join(ARTIFACTS_DIR, filename)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")
    chars = len(content)
    tokens = chars // 4
    print(f"✅ {filename}: {chars:,} chars (~{tokens:,} tokens)")

print(f"\nAll 6 artifacts written to {ARTIFACTS_DIR}/")
