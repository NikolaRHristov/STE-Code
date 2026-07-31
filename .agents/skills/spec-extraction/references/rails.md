# Process Rails — Error Prevention for All Orchestrators and Workers

> Each orchestrator and worker MUST validate against these rails before
> claiming any action complete. Rails are non-negotiable guardrails.

---

## RAIL 1: Stage Isolation

**Rule**: A process in Stage N MUST NOT write to Stage N+1 or Stage N-1 directories.

| Stage | Directory | Allowed Actions |
|-------|-----------|-----------------|
| 1 — Extract | `extracted/` | Write `w*-p*.md`. Read `spec/issue-09-2025/`. |
| 2 — Refine | `refined/` | Read `extracted/`, write `r*-p*.md`. |
| 3 — Merge | `merged/` | Read `refined/` (or `extracted/`), write to `merged/`. |
| 4 — Adapt | `adapted/` | Read `merged/`, write to `adapted/`. |
| 5 — Artifacts | `artifacts/` | Read `adapted/`, write `.txt` files. |

**Violation**: Writing adaptation files while extraction is in Stage 1.
**Violation**: Placing files in `ste-code/` root instead of a stage directory.
**Violation**: Reading from `extracted/` when `refined/` is available (Stage 3+).

## RAIL 2: Naming Convention

**Rule**: All worker output files MUST follow the exact naming pattern.

| Stage | Pattern | Example |
|-------|---------|---------|
| Extract | `wNNN-pPPPP-PPPP.md` | `w001-p1-4.md` |
| Refine | `rNNN-pPPPP-PPPP.md` | `r001-p1-4.md` |
| Adapt | `a-secN-ruleY.Z.md` | `a-sec1-rule1.1.md` |
| Artifacts | `ste-code-<name>.txt` | `ste-code-distilled-system-prompt.txt` |

**Violation**: `w1-sec1-rules.md` (old style — must be `w001-p1-4.md`).
**Violation**: `coding-rules-part1-sec1.md` (wrong stage, wrong naming).

## RAIL 3: Completion Integrity

**Rule**: NEVER claim a batch, stage, or phase complete without verification.

**Before claiming "Batch N complete":**
- [ ] All 3 output files exist on disk
- [ ] Each file > 3KB (>30 lines)
- [ ] Last 3 lines end cleanly (no mid-word truncation)
- [ ] Update PROGRESS.md with [x]

**Before claiming "Stage complete":**
- [ ] All files for that stage exist (e.g., 109/109 for extraction)
- [ ] Coverage audit passes (all 434 pages accounted for)
- [ ] Spot-check 3 random files for content fidelity

**Violation**: PLAN.md claiming "CORE ARTIFACTS COMPLETE ✅" when 288 pages unread.
**Violation**: PROGRESS.md showing [x] for a batch whose files don't exist.

## RAIL 4: Content Fidelity

**Rule**: NEVER fabricate, summarize, or adapt content that isn't backed by source data.

**Extraction workers**: Output EXACT spec text. Never:
- Add commentary ("This page describes...")
- Add modern terms not in the spec
- Summarize instead of extracting fully

**Refinement workers**: Reformat only. Never:
- Delete any word, number, or example
- Merge different examples into one
- Change rule numbers or section structure

**Adaptation workers**: Ground every claim. Never:
- Write an adapted rule without referencing the original rule from master.md
- Invent synonyms not in the original synonym table
- Claim a category count without verifying against master.md

**Fabrication detection signals** (if output contains any of these, it's fabricated):
- Modern software terms in spec extraction: "React", "Docker", "npm", "async/await"
- Commentary language: "This page describes", "The key point is", "In summary"
- Missing spec boilerplate: no "ASD-STE100" header
- Wrong facts: "22 categories", "deepseek-pro normalizes to flash", "hermes -z doesn't support file I/O"

## RAIL 5: Formatting Standards

**Rule**: All markdown output MUST follow these rules.

### Headings
```
✅ # Page N of M          ← Every file starts with this
✅ ## Section Title        ← Major sections
✅ ### Rule X.Y            ← Rule headings
✅ #### WORD (POS)         ← Dictionary entries (refined format)

❌ ### ASD-STE100          ← Proper names are not headings
❌ ### Heading\nText       ← NEVER glue heading to text
```

### Spacing
```
✅ ### Heading            ← Heading
✅                        ← BLANK LINE (mandatory)
✅ Content starts here    ← Content

❌ ### Heading            ← Heading
❌ Content starts here    ← NO blank line = GLUED
```

### Tables
```
✅ | Header | Header |    ← Header row
✅ |--------|--------|    ← Separator row  
✅ | Cell   | Cell   |    ← Data rows
✅                        ← BLANK LINE after table

❌ | Cell |\nNext text     ← No blank line after table
```

### STE/Non-STE Examples
```
✅ > **STE:** [example text]
✅ > **Non-STE:** [example text]

❌ STE: [text]             ← Must use blockquote + bold label
❌ Non-STE: [text] on same line as STE
```

### Dictionary Entries (refined format)
```
✅ #### WORD (POS) — APPROVED
✅ - **Meaning:** [text]
✅ - **Forms:** [form1, form2]
✅ - **STE:** [example]
✅ - **Non-STE:** [example]

❌ Word | Meaning merged in one column  ← Raw extraction format, not refined
```

## RAIL 6: Factual Correctness

**Rule**: These facts are immutable. Never claim otherwise.

| Fact | Wrong Claim (never make) |
|------|--------------------------|
| STE has 19 technical noun categories | "22 categories" |
| Model is `poolside/laguna-s-2.1:free` | "deepseek-pro" or "deepseek-v4-flash" |
| `hermes -z` supports file I/O | "hermes -z does not support file I/O" |
| 53 writing rules + 4 GR rules | 65 rules (Issue 6 count) |
| Output is `.md` files | "JSON structured data" |
| Stage directories are `extracted/`, `refined/`, etc. | "workers/" |

## RAIL 7: Progress Tracking

**Rule**: PROGRESS.md must reflect reality. Never lie to the tracker.

- Update PROGRESS.md AFTER verification, never before.
- If a worker fails, mark it [!] not [x].
- If re-extracting, revert [x] to [ ] until verified again.
- Timestamp all updates.

## RAIL 8: Error Recovery

**Rule**: When a mistake is detected, fix it. Do not hide it.

| Mistake | Recovery Action |
|---------|-----------------|
| Truncated worker output | Split page range in half, re-extract both |
| Fabricated content detected | Delete file, re-extract from spec |
| Wrong naming convention | Rename file to correct pattern |
| Missing PROGRESS.md update | Update immediately, note the correction |
| Premature adaptation files | Move to `_scratch/`, regenerate after extraction |
| Model reference wrong | Patch to correct model name |

---

## Quick Self-Check (run after every action)

```
□ Did I write to the correct stage directory?
□ Does my file follow the naming convention?
□ Did I verify before claiming complete?
□ Is my content backed by source data (not fabricated)?
□ Are my headings separated from text by blank lines?
□ Are my facts correct (19 categories, poolside/laguna-s-2.1:free, 53 rules)?
□ Did I update PROGRESS.md with the real status?
```
