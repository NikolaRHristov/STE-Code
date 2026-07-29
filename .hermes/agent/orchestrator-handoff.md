# STE-Code Continuation Prompt — For Fresh Orchestrator Session

> **Paste this entire block into a new Hermes session to continue the STE-Code pipeline.**
> The extraction and refinement phases are complete. Your job: produce the final artifacts.

---

## WHAT WAS ACCOMPLISHED

The 434-page ASD-STE100 Issue 9 specification has been fully extracted and refined
by a pipeline of 109 parallel `hermes -z` workers, each processing 4 pages.

### Pipeline State

| Stage | Location | Status | Count |
|-------|----------|--------|-------|
| Extract | `ste-code/extracted/` | ✅ 100% | 109 files, 912K |
| Refine | `ste-code/refined/` | ✅ 100% | 109 files, 880K |
| Merge | `ste-code/merged/` | ✅ | master.md + master-raw.md (710K) |
| Adapt | `ste-code/_scratch/` | ⚠️ v1 only | Needs re-do from refined data |
| Artifacts | `ste-code/_scratch/` | ⚠️ v1 only | Needs re-do from refined data |

### Key files you'll need:
- `ste-code/merged/master.md` — structural index mapping every rule to its extracted page
- `ste-code/merged/master-raw.md` — 710KB of raw concatenated spec text
- `ste-code/refined/r*.md` — 109 polished, reformatted markdown files (use these for adaptation!)
- `ste-code/PROGRESS.md` — extraction tracker (all checkboxes ticked)
- `ste-code/REFINE-PROGRESS.md` — refinement tracker (all checkboxes ticked)

### Skills available (load if needed):
- `skill_view(name='ste-code-adaptation')` — adaptation rules and category mapping
- `skill_view(name='ste-code-artifacts')` — artifact output specifications
- `skill_view(name='ste-code-merge')` — merge protocol
- `skill_view(name='agent-state-report')` — produce status reports

---

## WHAT YOU NEED TO DO (GATE 3-4)

### Phase 1: Read the Refined Data

Read these refined files to understand the full spec structure:
- `ste-code/refined/r001-p1-4.md` through `r012-p45-48.md` — front matter, TOC, Section 1 rules
- `ste-code/refined/r013-p49-52.md` through `r020-p77-80.md` — Sections 2-4 rules
- `ste-code/refined/r021-p81-84.md` through `r030-p117-120.md` — Sections 5-9 rules + GRs
- `ste-code/refined/r031-p121-124.md` through `r109-p433-434.md` — Dictionary entries + appendices

The refined files are clean, standardized markdown — much easier to work from than raw extraction.

### Phase 2: Adapt All 53 Rules for Code Domain

Produce these adaptation files in `ste-code/adapted/`:

**Part 1 — Coding Rules (follow ASD-STE100 structure exactly):**

1. `adapted/sec1-identifiers.md` — Rules 1.1-1.14 (Identifiers and Names)
   - 19 Technical Code Noun categories (adapted from STE's 19)
   - 4 Technical Code Verb categories
   - Every rule with code-domain examples (not aerospace)

2. `adapted/sec2-compound-ids.md` — Rules 2.1-2.2 (Compound Identifiers)
   - Max 3 components, shorter forms, hyphens

3. `adapted/sec3-functions.md` — Rules 3.1-3.7 (Functions and Operations)
   - Verb forms, tenses, active voice, -ing form restrictions

4. `adapted/sec4-statements.md` — Rules 4.1-4.5 (Statements and Expressions)
   - Short sentences, vertical lists, connecting words, articles

5. `adapted/sec5-procedural.md` — Rules 5.1-5.5 (Procedural Code Documentation)
   - 20-word max, one instruction per sentence, imperative form

6. `adapted/sec6-declarative.md` — Rules 6.1-6.6 (Declarative Code Documentation)
   - 25-word max, gradual information, key words, paragraphs

7. `adapted/sec7-safety.md` — Rules 7.1-7.3 (Error Handling)
   - BREAKING (was WARNING), DEPRECATED (was CAUTION), NOTE

8. `adapted/sec8-syntax.md` — Rules 8.1-8.7 (Syntax and Formatting)
   - No semicolons, hyphens, parentheses, word count rules

9. `adapted/sec9-practices.md` — Rules 9.1-9.4 + GR-1 through GR-8
   - Restructuring, approved words, phrasal verbs, consistency
   - That, with, pronouns, false friends, Latin abbreviations, inclusive language, possessive

**Part 2 — STE-Code Vocabulary (dictionary adaptation):**

10. `adapted/vocabulary.md` — Adapted dictionary with code-domain approved words
    - Canonical synonym table (60+ pairs: set up→configure, hit→call, etc.)
    - Polysemy resolution table (resolve, execute, render, deploy, etc.)
    - Anti-patterns list

### Phase 3: Produce Final Artifacts

Write these to `ste-code/artifacts/`:

1. `ste-code-distilled-system-prompt.md` (~1,400 tokens)
   - Standalone system prompt for any LLM
   - 14 core principles, synonym table, anti-patterns, quick reference

2. `ste-code-self-reading-manual.md` (~7,000 tokens)
   - S0-S8 sections: how to use, core principles, knowledge base (all rules),
     page-reading protocol, skill extraction, UML extraction, recursive questioning,
     output format, context management

3. `ste-code-extraction-methodology.md` (~1,400 tokens)
   - 6-pass pipeline, turn-by-turn protocol, edge cases

4. `ste-code-example-turn.md` (~500 tokens)
   - Worked example: non-STE comment → STE-Code transformation

5. `ste-code-deployment-guide.md`
   - Ollama, LM Studio, OpenAI, Claude, LangChain instructions

6. `README.md`
   - Project overview, quick start, architecture

---

## ADAPTATION RULES

### PRESERVE (unchanged from STE):
- Rule numbers (1.1 through 9.4, GR-1 through GR-8)
- Section organization (9 sections)
- Rule structure (imperative statement + explanatory text + examples)
- 6-pass pipeline architecture
- Dictionary architecture (APPROVED/UNAPPROVED with alternatives)

### REPLACE (adapted for code domain):
- Every STE/non-STE example → code documentation example
- 19 categories → code domain (see mapping below)
- Safety WARNING/CAUTION → BREAKING/DEPRECATED/NOTE

### Category Mapping:
| # | Original STE | STE-Code |
|---|-------------|----------|
| 1 | Parts information | Language keywords |
| 2 | Vehicles/machines | Frameworks and runtimes |
| 3 | Tools/equipment | Dev tools and build systems |
| 4 | Materials/consumables | Dependencies and packages |
| 5 | Facilities/locations | Deployment targets |
| 6 | Systems/components | Modules, classes, services |
| 7 | Math/scientific | Algorithmic terms |
| 8 | Navigation | Routing and state management |
| 9 | Numbers/units/time | Data sizes, time units |
| 10 | Quoted text | String literals, log output |
| 11 | Persons/organizations | Roles, teams, services |
| 12 | Body parts | UI/UX and accessibility |
| 13 | Personal effects | Configuration and preferences |
| 14 | Medical terms | Error states and diagnostics |
| 15 | Official documents | Spec files and configs |
| 16 | Environmental | Runtime conditions |
| 17 | Colors | Terminal colors, syntax highlighting |
| 18 | Damage terms | Bug/defect taxonomy |
| 19 | IT/telephony | Network, protocol, API terms |

---

## VERIFICATION CHECKLIST

After producing all files:
```bash
# Check file count
ls ste-code/adapted/*.md | wc -l  # should be 10
ls ste-code/artifacts/*.md | wc -l # should be 6

# Check no fabricated content
grep -l "TODO\|TBD\|placeholder" ste-code/adapted/*.md ste-code/artifacts/*.md
# Should return nothing

# Verify every rule number appears
grep -c "Rule [0-9]" ste-code/adapted/*.md
# Should show all 53 rules across the files

# Save progress
git add -A && git gcommit-hermes && git sync
```

---

## INFRASTRUCTURE

### Hermes worker pattern (if you need to launch more workers):
```bash
hermes -z "$(cat prompt.txt)" -m deepseek-pro --yolo
```
- Launch 3 at a time via `terminal(background=true, notify_on_complete=true)`
- Use `process(action='poll')` to check progress
- Git commit after each batch

### Key directories:
```
ste-code/
├── extracted/     ← 109 raw extraction files (SOURCE OF TRUTH)
├── refined/       ← 109 polished files (USE THESE FOR ADAPTATION)
├── merged/        ← master.md + master-raw.md
├── adapted/       ← YOUR OUTPUT — produce 10 adaptation files here
├── artifacts/     ← YOUR OUTPUT — produce 6 artifact files here
├── _scratch/      ← v1 drafts (reference only, not authoritative)
└── PROGRESS.md    ← update as you go

.hermes/
├── skills/spec-extraction/  ← 8 reusable skills
├── agent/                   ← state reports
└── feedback/                ← coordinator↔reviewer exchange
```

Good luck. The heavy lifting is done — 109 workers extracted every word. Now you make it shine.
