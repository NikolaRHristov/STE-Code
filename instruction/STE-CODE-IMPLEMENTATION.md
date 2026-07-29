# STE-Code: Simplified Technical English for Code — Full Implementation Instruction

> Paste this entire instruction into the target session. The agent should
> use parallel workers to process spec pages, then assemble the final artifacts.

---

## Phase 0: Parallel Worker Architecture (READ THIS FIRST)

You are the **coordinator agent**. You will NOT read all 434 pages sequentially yourself.
Instead, you will launch **parallel worker sessions** that each process a batch of pages.
Workers extract structured data and write results to shared files. You then merge all
worker output and produce the final STE-Code artifacts.

### Worker Specification

Each worker is a new Hermes session launched with:

```
hermes -z --model deepseek-pro "Read these spec pages: <page_range>. 
Extract: <extraction_task>. Output to: <output_file>."
```

**Rules for workers:**
- Always use `deepseek-pro` (NOT flash) — accuracy matters for spec extraction
- Each worker handles **exactly one batch** and outputs to one file
- Workers must NOT adapt anything — they extract raw spec data only
- Workers output structured JSON for machine-readable merging
- Main agent (you) polls workers, reads their output, merges, and adapts

### Work Planning

Before launching any workers, plan the batches. Here is the recommended split:

| Worker | Pages | Extraction Task | Output File |
|--------|-------|-----------------|-------------|
| W1 | 1–30 | Front matter, TOC, highlights, introduction, Section 1 rules (1.1–1.14) | `workers/w1-front-matter-rules-sec1.json` |
| W2 | 31–60 | Section 2-3 rules (2.1–2.3, 3.1–3.7), technical noun categories start | `workers/w2-rules-sec2-3.json` |
| W3 | 61–90 | Section 4-5 rules (4.1–4.4, 5.1–5.5), technical noun categories continue | `workers/w3-rules-sec4-5.json` |
| W4 | 91–120 | Section 6-7 rules (6.1–6.6, 7.1–7.3), technical noun categories complete | `workers/w4-rules-sec6-7.json` |
| W5 | 121–180 | Section 8-9 rules (8.1–8.7, 9.1–9.4, GR1–GR4), polysemy table | `workers/w5-rules-sec8-9.json` |
| W6 | 181–240 | Dictionary A–F entries, synonym table, approved meanings | `workers/w6-dict-a-f.json` |
| W7 | 241–300 | Dictionary G–P entries, transformation examples | `workers/w7-dict-g-p.json` |
| W8 | 301–360 | Dictionary Q–Z entries, remaining examples | `workers/w8-dict-q-z.json` |
| W9 | 361–434 | Appendices, index, change history, issue evolution data | `workers/w9-appendices.json` |

### Worker Prompt Template

For each worker, construct the prompt like this (replace `<<PLACEHOLDERS>>`):

```
hermes -z --model deepseek-pro "
You are a spec extraction worker. Your job is precise, not creative.

TASK: Read spec/issue-09-2025/page-<<START>>.md through page-<<END>>.md
and extract <<EXTRACTION_TASK>>.

OUTPUT FORMAT: Write ONLY valid JSON to <<OUTPUT_FILE>>. No markdown
wrapping, no explanations, no conversational text — just the JSON.
Use this schema:
{
  \"source_pages\": \"<<START>>-<<END>>\",
  \"task\": \"<<EXTRACTION_TASK>>\",
  \"rules\": [...],
  \"categories\": [...],
  \"dictionary_entries\": [...],
  \"synonyms\": [...],
  \"polysemy\": [...],
  \"examples\": [...],
  \"pipeline_steps\": [...],
  \"evolution_history\": [...]
}

Include all extracted data under the relevant keys. If a key's data
type is not present in your page range, use an empty array.

RULES:
- No adaptation. Extract the EXACT text from the spec pages.
- Preserve ALL rule numbers, ALL example pairs (STE and non-STE).
- For dictionary entries: include word, POS, approved meaning,
  approved forms, and alternatives EXACTLY as written.
- Do not summarize. Write every entry.
- Output ONLY the JSON. No preamble, no postscript.
"
```

### Worker Launch and Poll Protocol

Launch workers in **parallel batches of 3** to avoid overwhelming the system:

**Batch 1** (launch simultaneously):
```bash
hermes -z --model deepseek-pro "<worker-W1-prompt>" &
hermes -z --model deepseek-pro "<worker-W2-prompt>" &
hermes -z --model deepseek-pro "<worker-W3-prompt>" &
```

Wait for all 3 to complete (poll their output files for valid JSON), then:

**Batch 2**:
```bash
hermes -z --model deepseek-pro "<worker-W4-prompt>" &
hermes -z --model deepseek-pro "<worker-W5-prompt>" &
hermes -z --model deepseek-pro "<worker-W6-prompt>" &
```

**Batch 3**:
```bash
hermes -z --model deepseek-pro "<worker-W7-prompt>" &
hermes -z --model deepseek-pro "<worker-W8-prompt>" &
hermes -z --model deepseek-pro "<worker-W9-prompt>" &
```

### Merge Phase

After all 9 workers complete, read every `workers/w*.json` file.
Merge their extracted data into a single master state containing:
- All 53 rules with exact text and examples
- All 19 technical noun categories
- Complete dictionary entries
- Full synonym canonicalization table
- Complete polysemy resolution table
- All transformation pipeline steps
- Full evolution history

**Do not proceed to Phase 1 until this master state is complete.**

---

## Phase 1: Validate Master State Against Spec

With your merged master state, spot-check 10 random pages from the spec
against the extracted data. Verify:
- Rule text matches exactly
- Example pairs are complete
- Dictionary entries have all fields
- No data was lost in extraction

If discrepancies found, launch a correction worker for those specific pages.

---

## Phase 2: Produce STE-Code — The Complete Adaptation

You are creating **STE-Code**: Simplified Technical English for Code. This is the
coding-domain equivalent of ASD-STE100, preserving the exact same architecture
but adapted to software development documentation, API design, commit messages,
README files, inline comments, and code review language.

### WHAT TO PRESERVE (unchanged structure)

- **All 53 rules** — same rule numbers, same 9-section organization
- **The 6-pass transformation pipeline** (lexical lookup → classification → POS lock → meaning validation → grammar → consistency)
- **The dictionary architecture** — approved (UPPERCASE) vs unapproved (lowercase) with alternatives
- **The 19 categories** — same category structure, adapted content
- **Canonical synonym table** — same format, code-domain synonyms
- **Polysemy resolution table** — same format, code-domain entries
- **Safety instruction format** — adapted from WARNING/CAUTION to code security/breaking-change patterns
- **Output format** — ## COMPLIANCE STATUS / ## TECHNICAL OUTPUT / ## UML EXTRACTION / ## OPTIMIZATIONS

### WHAT TO REPLACE (adapted for code domain)

**Vocabulary** — Rewrite the ~875 approved words for code contexts:
- Variable naming conventions
- Function/method naming
- Documentation verbs (render, serialize, validate, dispatch, resolve)
- Review terms (approve, reject, request-changes, merge, rebase)
- Architecture terms (dependency, interface, contract, schema, endpoint)

**Examples** — Every STE/non-STE example pair becomes a code documentation example:
- Non-STE: "The function should be called and the return value needs to be checked"
- STE-Code: "Call the function. Check the return value."

**Technical noun categories** — Remap all 19:
| Original | STE-Code |
|----------|----------|
| 1. Parts information | Language keywords and reserved words |
| 2. Vehicles/machines | Frameworks and runtimes |
| 3. Tools and support equipment | Development tools and build systems |
| 4. Materials and consumables | Dependencies and packages |
| 5. Facilities and locations | Deployment targets and environments |
| 6. Systems and components | Modules, classes, and components |
| 7. Mathematical/scientific terms | Algorithmic and computational terms |
| 8. Navigation terms | Routing, pathing, and traversal terms |
| 9. Numbers/units/time | Data sizes, time units, numeric formats |
| 10. Quoted text | String literals, error messages, log text |
| 11. Persons/groups/organizations | Roles, teams, and services |
| 12. Parts of the body | N/A — replace with UI/UX interaction terms |
| 13. Personal effects | Configuration and preference terms |
| 14. Medical terms | Error states and diagnostic terms |
| 15. Official documents | Specification files and config formats |
| 16. Environmental conditions | Runtime conditions and states |
| 17. Colors | Terminal colors, syntax highlighting |
| 18. Damage terms | Bug, defect, and failure taxonomy |
| 19. IT and telephony terms | Network, protocol, and API terms |

---

## Phase 3: Output Two Artifact Sizes

### SHORT FORM (~1,200 tokens)
A system prompt that constrains any LLM to produce STE-Code compliant output.
Structure identically to `ste_distilled_system_prompt.txt`:
- Identity block
- 14 core principles (adapted)
- Canonical synonym table (adapted)
- Approved vocabulary policy (adapted)
- Document interaction protocol (adapted)
- Output format
- Anti-patterns

File: `ste-code-distilled-system-prompt.txt`

### LONG FORM (~7,000 tokens)
A self-reading manual with all 8 sections (S0–S8), following the exact structure
of `ste_self_reading_manual.txt`:
- S0: How to use this manual
- S1: Core STE-Code principles
- S2: Knowledge base (all 53 rules adapted, 19 categories, polysemy, pipeline)
- S3: Page-reading protocol
- S4: Skill extraction framework
- S5: UML extraction framework (code-specific UML: class diagrams, sequence diagrams)
- S6: Recursive questioning protocol (13 questions)
- S7: Output format
- S8: Context window management

File: `ste-code-self-reading-manual.txt`

---

## Phase 4: Supporting Artifacts

### Extraction Methodology (~1,400 tokens)
Turn-by-turn protocol adapted for code documents (READMEs, API specs, code reviews).

File: `ste-code-extraction-methodology.txt`

### Worked Example (~500 tokens)
Single-turn extraction showing a non-STE code comment transformed to STE-Code.

File: `ste-code-example-turn.txt`

### Deployment Guide
Instructions for deploying STE-Code as a system prompt in Ollama, LM Studio, Python.

File: `ste-code-deployment-guide.txt`

---

## Rules for the Agent

1. **Self-reference**: Re-read the original spec pages whenever you need exact rule text.
2. **One rule at a time**: Do not skip rules. Adapt each of the 53 rules fully.
3. **Output per section**: Write one file per completed section, not partial work.
4. **Verify against original**: Before outputting a rule, check the original text for accuracy.
5. **STE-Code is a proper subset**: Every STE-Code sentence must be valid English, just as STE is a proper subset of English.
6. **No placeholder text**: Every synonym, every polysemy entry, every example must be fully written. No "TODO" or "TBD."

---

## Output Directory Structure

```
ste-code/
├── workers/                                    # Worker extraction output
│   ├── w1-front-matter-rules-sec1.json
│   ├── w2-rules-sec2-3.json
│   ├── w3-rules-sec4-5.json
│   ├── w4-rules-sec6-7.json
│   ├── w5-rules-sec8-9.json
│   ├── w6-dict-a-f.json
│   ├── w7-dict-g-p.json
│   ├── w8-dict-q-z.json
│   └── w9-appendices.json
├── ste-code-distilled-system-prompt.txt     (~1,200 tokens)
├── ste-code-self-reading-manual.txt          (~7,000 tokens)
├── ste-code-extraction-methodology.txt       (~1,400 tokens)
├── ste-code-example-turn.txt                  (~500 tokens)
├── ste-code-deployment-guide.txt
└── README.md
```

## Phase Flow Summary

```
Phase 0:  Launch 9 parallel workers (batches of 3) → extract raw JSON
Phase 1:  Validate merged master state against random spec pages
Phase 2:  Plan adaptation: PRESERVE vs REPLACE mappings
Phase 3:  Write SHORT (~1,200 tokens) + LONG (~7,000 tokens) artifacts
Phase 4:  Write methodology, example, deployment guide
```
