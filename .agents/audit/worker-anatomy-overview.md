# STE-Code Worker Anatomy — Complete Technical Overview

## Single Worker Prompt File Structure

A worker prompt file contains 8 sections. Here is the full template for Pass 1 (Rule Examples):

```text
═══════════════════════════════════════════════════════════
SECTION 1: SYSTEM PROMPT (RULES)
═══════════════════════════════════════════════════════════
[Contents of ste-code/artifacts/ste-code-distilled-system-prompt.txt]
— 14 principles (P1-P14)
— Canonical synonym table (12 pairs → 30 expanded)
— 5 anti-patterns
— Output format rules

═══════════════════════════════════════════════════════════
SECTION 2: AGENT IDENTITY + PROTOCOL
═══════════════════════════════════════════════════════════
[Contents of .agents/agent/agent-4-continuation.md]
— Worker role: Expand, don't compress
— Pass-specific instructions (Pass 1: Rule Examples)
— Output format specification
— Deduplication rules
— Quality gates

═══════════════════════════════════════════════════════════
SECTION 3: TASK SPECIFICATION
═══════════════════════════════════════════════════════════
PASS: 1 — Rule Examples
TARGET: Generate 3-5 STE/non-STE code documentation example pairs for each rule
RULES TO PROCESS: a-sec1-rule1.1.md through a-sec1-rule1.14.md (Section 1)
OUTPUT FORMAT: JSON
  {
    "pass": "rule-examples",
    "batch": N,
    "rules_processed": ["rule-1.1", "rule-1.2", ...],
    "entries": [
      {
        "rule": "rule-1.1",
        "principle": "P1",
        "ste_example": "Use the authentication module.",
        "non_ste_example": "Leverage the auth stuff.",
        "explanation": "Replaced 'leverage' with 'use' and 'stuff' with specific noun."
      }
    ]
  }

═══════════════════════════════════════════════════════════
SECTION 4: INPUT CONTENT (THE THING TO EXPAND)
═══════════════════════════════════════════════════════════
[Contents of ste-code/adapted/a-sec1-rule1.1.md]
[Contents of ste-code/adapted/a-sec1-rule1.2.md]
...
[Contents of ste-code/adapted/a-sec1-rule1.14.md]

═══════════════════════════════════════════════════════════
SECTION 5: DEDUP BLACKLIST (DO NOT GENERATE THESE)
═══════════════════════════════════════════════════════════
EXISTING CODE EXAMPLES (from adapted files):
  "Use the authentication module to verify credentials." → "Leverage the auth system."
  "Call the API endpoint with a valid token." → "Hit the endpoint with a good token."
  ...

EXISTING AEROSPACE EXAMPLES (from master.md):
  "Install the three auxiliary screws (2) in the flange." → "..."
  ...

PREVIOUSLY GENERATED (from expanded/):
  [empty for first batch — populated from previous batches]

═══════════════════════════════════════════════════════════
SECTION 6: REFERENCE DATA (CONTEXT)
═══════════════════════════════════════════════════════════
CODE DICTIONARY (excerpt):
  [Top 50 entries from SCE/data/vocabulary/code-dictionary.json]
  
SYNONYM TABLE:
  [SCE/core/categories/synonym-table.json — all 30 pairs]

CATEGORY MAPPING (excerpt):
  [19 categories with examples]

═══════════════════════════════════════════════════════════
SECTION 7: EXECUTION INSTRUCTIONS
═══════════════════════════════════════════════════════════
1. Read each adapted rule file in SECTION 4.
2. For each rule, identify the aerospace example pattern.
3. Generate 3-5 NEW code-domain examples that:
   a. Follow the same rule (same principle violation → same fix)
   b. Use code-domain terminology (server, API, function, endpoint)
   c. Replace EVERY aerospace term with a code equivalent
   d. Do NOT match any entry in SECTION 5 (dedup blacklist)
   e. Include an explanation of which principle was applied
4. Write the output as valid JSON to stdout.
5. Do NOT create any files. Output inline only.

═══════════════════════════════════════════════════════════
SECTION 8: VERIFICATION CHECKLIST
═══════════════════════════════════════════════════════════
Before output, verify:
[ ] At least 3 examples per rule generated
[ ] No aerospace terms (engine, ream, flange, aircraft, etc.)
[ ] No examples match SECTION 5 blacklist
[ ] Every example references the correct principle (P1-P14)
[ ] All JSON is valid
[ ] Every non_ste_example contains an actual violation
[ ] Every ste_example fixes that violation
```

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     INPUT LAYER                              │
├─────────────────────────────────────────────────────────────┤
│ spec/issue-09-2025.pdf (3.1MB, 434 pages)                   │
│   ↓ parsed page-by-page                                     │
│ spec/issue-09-2025/page-0001.md ... page-0434.md            │
│   ↓ extracted by Agent #1 (109 workers, batches of 3)       │
│ ste-code/extracted/w001-p1-4.md ... w109-p433-434.md        │
│   ↓ refined by Agent #2 (109 workers, 9 formatting rules)   │
│ ste-code/refined/r001-p1-4.md ... r109-p433-434.md          │
│   ↓ merged by Agent #4 Stage 3                              │
│ ste-code/grouped/master.md (20,794 lines, deduplicated)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   ADAPTATION LAYER                           │
├─────────────────────────────────────────────────────────────┤
│ ste-code/adapted/ (57 files, 9,400 lines)                   │
│   ├── a-sec1-rule1.1.md through a-sec1-rule1.14.md (14)    │
│   ├── a-sec2-rule2.1.md through a-sec2-rule2.2.md (2)      │
│   ├── a-sec3-rule3.1.md through a-sec3-rule3.7.md (7)      │
│   ├── a-sec4-rule4.1.md through a-sec4-rule4.5.md (5)      │
│   ├── a-sec5-rule5.1.md through a-sec5-rule5.5.md (5)      │
│   ├── a-sec6-rule6.1.md through a-sec6-rule6.5.md (5)      │
│   ├── a-sec7-rule7.1.md through a-sec7-rule7.3.md (3)      │
│   ├── a-sec8-rule8.1.md through a-sec8-rule8.6.md (6)      │
│   ├── a-sec9-rule9.1.md ... a-sec9-gr4.md (8)              │
│   ├── a-categories.md (19 categories)                       │
│   └── a-dictionary.md (5,943 lines, 1,212 code pairs)      │
│                                                              │
│ AGENT #4 EXPANSION (5 PASSES)                                │
│   ↓ Pass 1: 3-5 code examples per rule → expanded/          │
│   ↓ Pass 2: Dictionary depth → code-dictionary-mapping.json │
│   ↓ Pass 3: Category entries → category-entries.json        │
│   ↓ Pass 4: Anti-patterns → anti-patterns.json              │
│   ↓ Pass 5: Paradigm examples → paradigm-examples.json      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   ARTIFACTS LAYER                            │
├─────────────────────────────────────────────────────────────┤
│ ste-code/artifacts/ (6 files, regenerated from expanded)    │
│   1. ste-code-distilled-system-prompt.txt (~3K tokens)      │
│   2. ste-code-self-reading-manual.txt (~12K tokens)         │
│   3. ste-code-extraction-methodology.txt (~1.4K tokens)     │
│   4. ste-code-example-turn.txt (~1K tokens)                 │
│   5. ste-code-deployment-guide.txt (~1.8K tokens)           │
│   6. README.md (~1K tokens)                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   SCE LAYER (structured)                     │
├─────────────────────────────────────────────────────────────┤
│ SCE/ (35 files, ~100KB)                                     │
│   core/                                                      │
│   ├── categories/  synonym-table.json (30 pairs)            │
│   │                noun-categories.json (19 cats, 289 ex)   │
│   │                verb-categories.json (4 cats)             │
│   │                generated/ (190 terms, 10 anti-patterns) │
│   └── rules/       README.md (55 rules indexed)             │
│   data/                                                      │
│   └── vocabulary/  code-dictionary.json (175 entries)       │
│                    approved-verbs.json (35 entries)          │
│                    approved-adjectives.json                  │
│                    generated/ (15 verbs, 10 adjectives)      │
│   compute/                                                   │
│   ├── agentic/     rails.json, gate-conditions.json         │
│   │                worker-contract.json                      │
│   ├── prompts/     compliance-check, rule-adaptation        │
│   ├── schemas/     rule-frontmatter, vocabulary-entry       │
│   └── generated/   anti-patterns-batch-001.json (10)        │
│   narratives/                                                │
│   ├── system-prompts/  micro (500 tok), full (4K tok)       │
│   │                    agentic (2.5K), developer (2K)       │
│   └── examples/     commit-message, readme-section          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   AGENTS LAYER                               │
├─────────────────────────────────────────────────────────────┤
│ .agents/                                                     │
│   agent/     agent-1 through agent-9 (role definitions)     │
│   skills/    12 skills (extraction, refinement, ...)        │
│   benchmark/ 59 tests, 14 categories, orchestrator          │
│   references/ rails, worker-grid, category-mapping, ...     │
│   state/     PROGRESS.md, EXTENSION-PROGRESS.md, ...        │
│   audit/     audit reports, state reports, maturity audit   │
│   uml/       5 pipeline diagrams                             │
│   prompts/   worker prompts (adapt, enrich, refine, OSS)    │
│   rewrites/  level-{1,2,3,4}/ (Agent #7 output)            │
└─────────────────────────────────────────────────────────────┘
```

## Worker Count & Batch Flow

| Layer | Workers | Batch Size | Batches | Total Time |
|-------|:------:|:----------:|:------:|:----------:|
| Extraction (Agent #1) | 109 | 3 | 37 | ~30 min |
| Refinement (Agent #2) | 109 | 3 | 37 | ~30 min |
| Merge (Agent #4 Stage 3) | N/A | — | — | Manual |
| Adaptation (Agent #4 Stage 4) | 55 | — | — | Manual |
| **Expansion Pass 1** | **165-275** | 3 | **55-92** | **~90 min** |
| Expansion Pass 2 | 55-110 | 3 | 19-37 | ~45 min |
| Expansion Pass 3 | 19 | 3 | 7 | ~15 min |
| Expansion Pass 4 | 5-10 | 3 | 2-4 | ~5 min |
| Expansion Pass 5 | 6 | 3 | 2 | ~5 min |
| Artifacts (Stage 5) | 6 | 3 | 2 | ~5 min |
| **Total** | ~**500** | — | ~**150** | **~4 hours** |

## Per-Worker Data Flow

```
Worker N receives:
  ├── System prompt (50 lines, ~500 tokens)
  ├── Agent protocol (140 lines, ~2K tokens)
  ├── Task spec (20 lines, ~300 tokens)
  ├── Input content (3-5 adapted rule files, ~2K tokens each)
  ├── Dedup blacklist (growing — starts empty, accumulates from prior batches)
  ├── Reference data (dictionary excerpt, synonym table, categories)
  ├── Execution instructions (10 lines)
  └── Verification checklist (7 items)

Total per worker: ~10-15K tokens input

Worker N outputs:
  └── JSON file (50-100 entries, 5-15KB)
       Written to: ste-code/adapted/expanded/<pass>-batch-NNN.json
       Dedup blacklist updated for next batch
```

## Moving Parts Summary

| Part | Count | Flow |
|------|:-----:|------|
| Source pages | 434 | PDF → MD extraction |
| Extraction workers | 109 | 4 pages each, 37 batches |
| Refinement workers | 109 | 9 formatting rules, 37 batches |
| Adapted rule files | 57 | 1:1 translation of 53 rules + 4 GR |
| Expansion passes | 5 | Each expands a dimension |
| Expansion workers | ~275 | 3 per batch, ~92 batches |
| Artifact files | 6 | Regenerated from expanded content |
| SCE structured files | 35 | 4 strata, machine-readable |
| Agent definitions | 9 | Role-based, reusable |
| Skills | 12 | Capability protocols |
| Benchmark tests | 59 | 14 categories, automated scoring |
| Output directories | 15+ | Isolated per stage |
| Cross-reference links | 200+ | Between adapted rules and master |
| Dedup entries | 4,945+ | Growing with each batch |
