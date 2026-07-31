# STE-Code Mission Plan — Complete Launch Protocol

> **Version**: 3.0 | **Date**: 2026-07-30
> **Purpose**: Single authoritative document. All orchestrators, reviewers, auditors,
> and external collaborators read this first. Executable from scratch.

---

## TERMINOLOGY MAP

All terms used throughout this project. Agents must use these exact terms.

### Pipeline Stages

| Term | Directory | Definition |
|------|-----------|------------|
| **Extraction** | `ste-code/extracted/` | Stage 1: Raw text extraction from ASD-STE100 spec pages |
| **Refinement** | `ste-code/refined/` | Stage 2: Formatting raw extraction into clean markdown |
| **Merge** | `ste-code/merged/` | Stage 3: Concatenate, deduplicate, organize into master.md |
| **Adaptation** | `ste-code/adapted/` | Stage 4: Transform STE rules into STE-Code (coding domain) |
| **Artifacts** | `ste-code/artifacts/` | Stage 5: Generate 6 final .txt output files |

### Agent Roles

| Term | Definition |
|------|------------|
| **Extraction Orchestrator** | Launches workers to read spec pages and extract raw text |
| **Refinement Orchestrator** | Launches workers to reformat extracted text into clean markdown |
| **Execution Auditor** | Hidden agent that verifies claims against disk evidence, auto-fixes safe errors |
| **Reviewer** | Human or AI that reviews quality and provides feedback |
| **Worker** | Single `hermes -z` session processing 4 spec pages |

### Naming Conventions

| Pattern | Usage | Example |
|---------|-------|---------|
| `wNNN-pPPPP-PPPP.md` | Extraction output | `w001-p1-4.md` |
| `rNNN-pPPPP-PPPP.md` | Refinement output | `r001-p1-4.md` |
| `a-secN-ruleY.Z.md` | Adaptation output | `a-sec1-rule1.1.md` |
| `ste-code-<name>.txt` | Final artifacts | `ste-code-distilled-system-prompt.txt` |
| `audit-YYYYMMDD-HHMMSS.md` | Audit reports | `audit-20260730-003400.md` |
| `state-YYYYMMDD-HHMMSS.md` | State snapshots | `state-20260730-004500.md` |

### Factual Constants (immutable)

| Constant | Value | Never Claim |
|----------|-------|-------------|
| STE technical noun categories | 19 original → 17 code-domain extensions | "22 categories" |
| STE writing rules | 53 original → 51 adapted + 4 GR |
| Spec pages | 434 | — |
| Spec version | Issue 9, January 2025 | — |
| Worker model | `poolside/laguna-s-2.1:free` | "deepseek-pro" or "flash" |
| Workers per batch | 3 | — |
| Pages per worker | 4 | — |
| Total workers | 109 | — |
| Total batches | 37 | — |

### Directory Map

| Path | Type | Contents |
|------|------|----------|
| `ste-code/extracted/` | Data | 109 raw extraction .md files |
| `ste-code/refined/` | Data | 109 formatted .md files |
| `ste-code/merged/` | Data | master-raw.md, master.md |
| `ste-code/adapted/` | Data | Per-rule adaptation .md files |
| `ste-code/artifacts/` | Data | 6 final .txt artifact files |
| `ste-code/README.md` | Data | Pipeline documentation |
| `.agents/state/` | Workflow | PROGRESS.md, REFINE-PROGRESS.md |
| `.agents/audit/` | Workflow | Audit reports, state snapshots |
| `.agents/prompts/refine/` | Workflow | 109 refinement worker prompts |
| `.agents/tools/quality/` | Workflow | verify-batch.sh, check-rails.py |
| `.agents/feedback/` | Workflow | exchange.md (orchestrator↔reviewer) |
| `.agents/skills/` | Workflow | 8 SKILL.md files + references |
| `.agents/_scratch/` | Workflow | Quarantined premature files |
| `spec/issue-09-2025/` | Source | 434 page .md files |
| `spec/issue-07-2017/` | Source | 382 page .md files |
| `instruction/` | Reference | STE-CODE-IMPLEMENTATION.md |

---

## MISSION HISTORY

### Phase 0 — Foundation (2026-07-29)

- Downloaded ASD-STE100 Issue 7 (382pp) and Issue 9 (434pp) PDFs
- Extracted all PDFs to individual page markdown files (840 pages total)
- Created 8 extracted reference documents from conversation analysis
- Named: 01-ste-introduction.md through 08-self-reading-manual.md

### Phase 1 — Architecture Design (2026-07-29)

- Designed the 5-stage pipeline: Extract → Refine → Merge → Adapt → Artifacts
- Created initial system prompt, extraction methodology, and worked example
- Established PRESERVE/REPLACE rules for STE→STE-Code adaptation
- Mapped 19 STE categories to 19 STE-Code categories

### Phase 2 — First Attempt & Corrections (2026-07-29)

- **Error**: Agent fabricated 6 artifact files before extraction complete
- **Error**: Claimed "22 categories" — corrected to 19
- **Error**: Claimed "deepseek-pro normalizes to flash" — corrected to `poolside/laguna-s-2.1:free`
- **Error**: Agent claimed "CORE ARTIFACTS COMPLETE" with 288 pages unread
- **Correction**: Created v2/v3 protocol with hard gates and verification

### Phase 3 — Worker Swarm (2026-07-30)

- Extraction orchestrator launched: 109 workers, 37 batches of 3
- **Complete**: All 109 extraction workers finished (434/434 pages)
- Refinement orchestrator launched: 54 prompts generated, ~54 files refined
- **Status**: Refinement at ~50% (54/109), remaining prompts need generation

### Phase 4 — Rails & Quality (2026-07-30)

- Created 8 immutable rails preventing common mistake classes
- Created worker rails (10 self-checks per worker)
- Created batch verification script and rails compliance checker
- Separated data (`ste-code/`) from workflow (`.agents/`)
- Created agent state report skill for standardized status reporting

---

## CURRENT STATE

```
Stage 1 — Extraction:   ✅ 109/109 (100%)   434/434 pages
Stage 2 — Refinement:   🟢 ~54/109 (~50%)   ~216/434 pages
Stage 3 — Merge:        🟡 master-raw.md exists, needs dedup
Stage 4 — Adaptation:   ⬜ Pending
Stage 5 — Artifacts:    ⬜ Pending
```

**Active**: Refinement orchestrator processing batches
**Blocked**: Nothing
**Next**: Complete refinement, run merge, begin adaptation

---

## EXECUTION FROM SCRATCH

### Prerequisites

```bash
# Verify spec files exist
ls spec/issue-09-2025/page-0001.md  # Must exist
ls spec/issue-09-2025/page-0434.md  # Must exist

# Verify model available
hermes config | grep default  # Should be poolside/laguna-s-2.1:free
```

### Step 1: Directory Setup

```bash
mkdir -p ste-code/{extracted,refined,merged,adapted,artifacts}
mkdir -p .agents/{state,audit,prompts/refine,scripts,feedback,_scratch}
```

### Step 2: Launch Extraction (109 workers, 37 batches)

```bash
# Generate 109 worker prompts (each: read 4 spec pages, write to extracted/)
# Launch in batches of 3:
hermes -z "$(cat .agents/prompts/refine/r001-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
hermes -z "$(cat .agents/prompts/refine/r002-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
hermes -z "$(cat .agents/prompts/refine/r003-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &

# After each batch:
bash .agents/tools/quality/verify-batch.sh extracted w w001 w002 w003
# Update .agents/state/PROGRESS.md
```

### Step 3: Launch Refinement (109 workers, 37 batches)

```bash
# Generate 109 refinement prompts (each: read extracted/NNN, write refined/NNN)
# Launch same batch pattern as extraction
# After each batch:
bash .agents/tools/quality/verify-batch.sh refined r r001 r002 r003
```

### Step 4: Merge

```bash
cat ste-code/refined/r*-p*.md > ste-code/merged/master-raw.md
# Deduplicate, organize by section, validate completeness
# Output: ste-code/merged/master.md
```

### Step 5: Adapt

```bash
# For each of 53 rules in master.md:
# Read original rule text + examples
# Produce STE-Code adaptation preserving rule number and structure
# Write to ste-code/adapted/a-secN-ruleY.Z.md
```

### Step 6: Generate Artifacts

```bash
# Write 6 files to ste-code/artifacts/:
# 1. ste-code-distilled-system-prompt.txt (~1,200 tokens)
# 2. ste-code-self-reading-manual.txt (~7,000 tokens)
# 3. ste-code-extraction-methodology.txt (~1,400 tokens)
# 4. ste-code-example-turn.txt (~500 tokens)
# 5. ste-code-deployment-guide.txt
# 6. README.md
```

### Quality Gates (run after each step)

```bash
# Rails compliance
python3 .agents/tools/quality/check-rails.py

# State report
# Trigger any agent: "state" → writes to .agents/audit/state-YYYYMMDD-HHMMSS.md

# Full audit (hidden agent)
# Launch: "You are the Execution Auditor. Audit all claims. Fix safe errors."
```

---

## SKILL MAP

| Skill | File | Role |
|-------|------|------|
| `ste-code-workers` | `SKILL.md` | Extraction orchestrator — launch 109 workers |
| `ste-code-refine` | `SKILL.md` | Refinement orchestrator — format raw extraction |
| `ste-code-merge` | `SKILL.md` | Merge phase — concatenate, deduplicate, organize |
| `ste-code-validate` | `SKILL.md` | Validation — per-batch and full-extraction checks |
| `ste-code-adaptation` | `SKILL.md` | Adaptation — STE→STE-Code rule transformation |
| `ste-code-artifacts` | `SKILL.md` | Artifact generation — 6 final .txt files |
| `execution-auditor` | `SKILL.md` | Hidden auditor — verify claims, auto-fix errors |
| `agent-state-report` | `SKILL.md` | State reporting — standardized full-page status |

---

## RAILS (8 Immutable Guardrails)

| # | Rail | Prevents |
|---|------|----------|
| R1 | Stage Isolation | Writing to wrong stage directory |
| R2 | Naming Convention | Mixed old/new file names |
| R3 | Completion Integrity | Claiming done without verification |
| R4 | Content Fidelity | Fabrication, summarization, commentary |
| R5 | Formatting Standards | Glued headings, missing blank lines |
| R6 | Factual Correctness | Wrong category count, wrong model |
| R7 | Progress Tracking | PROGRESS.md not reflecting reality |
| R8 | Error Recovery | Hiding instead of fixing mistakes |

Full details: `.agents/skills/references/rails.md`

---

## REFERENCES

| File | Content |
|------|---------|
| `.agents/skills/references/worker-grid.md` | 109-worker batch grid |
| `.agents/skills/references/section-types.md` | Page type classification |
| `.agents/skills/references/worker-rails.md` | Worker-level self-checks |
| `.agents/skills/references/quality-checklist.md` | Per-batch checklist |
| `.agents/skills/references/category-mapping.md` | 19-category STE→STE-Code map |
| `.agents/skills/references/rails.md` | 8 immutable guardrails |
| `.agents/references/idempotency-baseline.md` | Worker idempotency standard — Tier 1/2/3 checks |
| `.agents/feedback/exchange.md` | Orchestrator↔Reviewer communication |

---

## CANONICAL TOOLS (Phase A+ worker launching)

**Use these. Only these.**

| Tool | Path | Purpose |
|------|------|---------|
| Oneshot wrapper | `.agents/tools/lib/hermes-oneshot-wrapper.py` | Calls AIAgent directly. Reads prompt from file, deletes it after. No CLI, no TUI. |
| Launch worker | `.agents/tools/shared/launch-worker.sh` | Shell wrapper: auto-detects hermes venv, calls oneshot wrapper. Supports background with output capture. |
| Telemetry worker | `.agents/tools/shared/telemetry-worker.py` | Per-worker JSON telemetry in `.agents/telemetry/`. **Note: currently uses `hermes -z` CLI — migrate to oneshot wrapper.** |
| Prompt generator | `.agents/tools/runners/phase-a-gen.py` | Generates enhanced prompts from maturity-fix templates. |

**Anti-patterns (DO NOT USE):**
- ❌ `hermes -z "$(cat file)"` in `terminal(background=true)` — opens TUI, does not process
- ❌ `subprocess.Popen(["hermes", "-z", ...])` — unreliable stdout capture
- ❌ Custom Python wrappers that call `hermes -z` via subprocess — use oneshot wrapper instead

## AGENT RULE ACCESS

All agents have `read_file` access. When applying STE-Code rules:

1. **Consult the deepened rules directly:** `ste-code/adapted/a-secN-ruleX.Y.md` (51 files)
2. **Check the dictionary:** `ste-code/adapted/a-dictionary.md` (198KB, 5,943 lines)
3. **Verify synonyms:** `ste-code/data/synonym-table.json`
4. **Reference templates:** `ste-code/templates/ste-code-*.md` (4 levels)

Agents SHOULD read specific rule files when uncertain about rule application. The benchmark workers and all pipeline agents have this capability enabled.
