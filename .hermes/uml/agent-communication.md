# Agent Communication Architecture — STE-Code Pipeline

> Mermaid diagrams documenting coordination across the 4-agent pipeline.
> All communication flows through `.hermes/feedback/exchange.md` (structured turns)
> and `.hermes/audit/state-*.md` (immutable state snapshots).
> Audit reports live at `.hermes/audit/audit-*.md` (append-only evidence log).

---

## 1. AGENT ROLES — Handoff Chain

```mermaid
sequenceDiagram
    participant U as 👤 User / Reviewer
    participant A1 as 🤖 Agent #1<br/>Extraction Orchestrator
    participant A2 as 🤖 Agent #2<br/>Refinement Orchestrator
    participant A3 as 🔍 Agent #3<br/>Execution Auditor
    participant A4 as 🤖 Agent #4<br/>Continuation Orchestrator
    participant FS as 📁 Filesystem<br/>(ste-code/)
    participant EX as 💬 Exchange<br/>(.hermes/feedback/exchange.md)

    Note over A1,A4: === STAGE 1: EXTRACTION (434 pages, 109 workers) ===

    U->>A1: Launch extraction swarm<br/>"Extract all 434 pages via hermes -z workers"
    A1->>FS: mkdir ste-code/extracted/ ste-code/prompts/
    loop 37 batches × 3 workers
        A1->>A1: Write prompt → ste-code/prompts/wNNN-prompt.txt
        A1->>FS: hermes -z "$(cat prompt.txt)" --yolo (bg+notify)
        A1->>FS: Wait for all 3 workers → verify output >3KB
        A1->>FS: git gcommit-hermes
        A1->>FS: Update PROGRESS.md [x] WNNN
    end
    A1->>FS: python3 check-rails.py (R1-R8, all 4 checks)
    A1->>EX: Signal: "EXTRACTION PHASE COMPLETE. 109/109 ✅"
    A1->>FS: Write state report → .hermes/audit/state-*.md

    Note over A1,A4: === GATE 1: Extraction verified → handoff to Refinement ===

    A3->>FS: Audit: find extracted/*.md | wc -l → 109
    A3->>FS: Audit: grep fabrication patterns, zero-byte check
    A3->>EX: Flag: PROGRESS.md was 31 batches behind (🔴 CRITICAL)
    A3->>FS: Auto-fix: sync PROGRESS.md with disk reality
    EX-->>A2: Read exchange: Stage 1 done, 109 files ready

    Note over A1,A4: === STAGE 2: REFINEMENT (9 rules, zero content loss) ===

    A2->>FS: mkdir ste-code/refined/ .hermes/prompts/refine/
    A2->>FS: Verify 109 extracted files exist
    loop 37 batches × 3 workers
        A2->>A2: Generate prompt with ALL 9 refinement rules (no abbreviations)
        A2->>FS: hermes -z "$(cat .hermes/prompts/refine/rNNN-prompt.txt)" --yolo
        A2->>FS: Wait → verify >3KB, no truncation, 9 rules applied
        A2->>FS: git commit; Update REFINE-PROGRESS.md
    end

    A2->>FS: Verify: 109 refined files, zero content loss (21,852 lines)
    A2->>FS: Write state report → .hermes/audit/state-*.md
    A2->>EX: Signal: "REFINEMENT COMPLETE. 109/109 ✅"

    Note over A1,A4: === GATE 2: Refinement verified → handoff to Continuation ===

    A3->>FS: Audit: find refined/*.md | wc -l → 109
    A3->>FS: Audit: verify r029, r031 gaps recovered
    A3->>EX: Flag: 6 artifact files in root are FABRICATED (🔴)
    EX-->>A4: Read exchange: Stage 2 done, Stages 3-5 ready

    Note over A1,A4: === STAGES 3-5: MERGE → ADAPT → ARTIFACTS ===

    A4->>FS: Stage 3: concat 109 refined → master-raw.md
    A4->>FS: Deduplicate, organize by section → master.md
    A4->>FS: Validate: 53 rules, 19 categories, dict entries
    A4->>EX: Signal: "Stage 3 MERGE complete"

    A4->>FS: Stage 4: Adapt STE rules → code domain
    A4->>FS: 19-category mapping applied; examples replaced
    A4->>FS: Verify: every rule references master.md source
    A4->>EX: Signal: "Stage 4 ADAPTATION complete"

    A4->>FS: Stage 5: Generate 6 artifact files
    A4->>FS: Quality gates: token budgets, cross-references, anti-fabrication
    A4->>EX: Signal: "Stage 5 ARTIFACTS complete. Pipeline done."

    A3->>FS: Final audit: verify all 6 artifacts from refined data
    A3->>EX: Final report: pipeline dashboard 100% ✅
```

---

## 2. FEEDBACK PROTOCOL — Exchange File Turns

```mermaid
sequenceDiagram
    participant A as Any Agent
    participant EX as .hermes/feedback/exchange.md
    participant R as Reviewer / Other Agents

    Note over A,R: === TURN-BASED PROTOCOL ===

    A->>EX: APPEND new turn<br/>"## Orchestrator → Reviewer (Turn N)"
    A->>EX: WRITE structured section:<br/>- Current state<br/>- What was done<br/>- What needs verification<br/>- Any errors/blockers

    R->>EX: READ all turns to understand context
    R->>R: Cross-reference claims vs evidence
    R->>EX: APPEND response turn<br/>"## Reviewer → Orchestrator (Turn N)"

    Note over A,R: === EXCHANGE FORMAT ===

    A->>EX: Each agent writes in standard format:<br/>## [Role] → [Role] (Turn N)<br/>## [Role] → [Role] (Turn N) — YYYY-MM-DD [Summary Tag]

    Note over A,R: === EXCHANGE CONTENT RULES ===

    A->>EX: Include: worker counts (N/109), percentages,<br/>batch status (✅/🟢/[ ]), file sizes, lines, gaps
    A->>EX: Include: tracking doc sync status, stale file warnings
    A->>EX: Include: next actions, what other agents should verify
    A->>EX: NEVER fabricate progress — auditor cross-references against disk

    Note over A,R: === REAL EXCHANGE TURNS (from exchange.md) ===

    R->>EX: Turn 1: Reviewer flags W6-W9 missing,<br/>.md not .json, no PROGRESS.md,<br/>6 fabricated artifacts

    A->>EX: Turn 1 (reply): Workers WERE launched,<br/>.md was user directive, PROGRESS.md created

    A->>EX: Turn 2: STRATEGY REVISION — switching to 4pp/worker<br/>109 workers, 37 batches of 3

    R->>EX: Turn 2 (reply): v2 protocol — claimed hermes -z<br/>doesn't support file I/O (WRONG)

    A->>EX: Turn 3: v3 CORRECTION — proved hermes -z works<br/>W0 test wrote "OK" successfully<br/>v3 protocol now in STE-CODE-IMPLEMENTATION.md

    A3->>EX: Turn 4: AUDIT UPDATE — PROGRESS.md was 26 batches behind<br/>Extraction was 78/109 (not 78 claimed)<br/>Refinement was 11/109

    A3->>EX: Turn 5: RE-AUDIT — EXTRACTION COMPLETE 🎉<br/>109/109 workers, all 434 pages, 10,927 lines<br/>Refinement at 30/109 with gap notation

    A2->>EX: Turn 6: REFINEMENT COMPLETE 🎉<br/>109/109 workers, 21,852 lines, all 9 rules<br/>Signals Stages 3-4-5 ready to begin
```

---

## 3. STATE REPORTING — agent-state-report Skill

```mermaid
flowchart TD
    TRIGGER["🗣️ Trigger Words<br/>'state', 'status', 'report',<br/>'where are we', 'progress'"]
    SKILL["📄 agent-state-report/SKILL.md<br/>Standardized 8-section format"]
    SHELL["💻 Run shell commands<br/>(never estimate from memory)"]
    FORMAT["📋 Fill all 8 sections:<br/>1. Agent Identity<br/>2. Pipeline Status<br/>3. Active Workers<br/>4. Errors & Blockers<br/>5. Rails Compliance<br/>6. Files on Disk<br/>7. Next Actions<br/>8. Git State"]

    TRIGGER --> SKILL
    SKILL --> SHELL
    SHELL --> FORMAT

    FORMAT --> ID["1️⃣ Agent Identity<br/>Role, Session ID, Last Action,<br/>Time Since Last Batch"]
    FORMAT --> PS["2️⃣ Pipeline Status<br/>5-stage table: expected vs actual,<br/>percentages, ✅/🟢/⬜"]
    FORMAT --> AW["3️⃣ Active Workers<br/>Worker ID, Pages, Status,<br/>Output Size, Issues"]
    FORMAT --> EB["4️⃣ Errors & Blockers<br/>🔴 Critical / 🟠 Error / 🟡 Warning"]
    FORMAT --> RC["5️⃣ Rails Compliance<br/>R1-R8: PASS/FAIL per rail<br/>with issues detail"]
    FORMAT --> FD["6️⃣ Files on Disk<br/>find/du/wc commands —<br/>verified counts + sizes"]
    FORMAT --> NA["7️⃣ Next Actions<br/>Prioritized: immediate,<br/>next batch, pending, blocked"]
    FORMAT --> GS["8️⃣ Git State<br/>git status --short<br/>git log --oneline -3"]

    SHELL --> WRITE["💾 Write to .hermes/audit/state-YYYYMMDD-HHMMSS.md<br/>(immutable, timestamped)"]
    WRITE --> SYNC["🔄 If discrepancies found:<br/>update PROGRESS.md to match disk reality"]

    subgraph AUDIT_TRAIL["📁 Immutable Audit Trail"]
        direction LR
        A1[".hermes/audit/state-20260729-214707.md"]
        A2[".hermes/audit/state-20260730-000000.md"]
        A3[".hermes/audit/state-20260730-004500.md"]
        A4[".hermes/audit/audit-20260729-211611.md"]
        A5[".hermes/audit/audit-20260729-212052.md"]
        A6[".hermes/audit/audit-20260729-213422.md"]
    end

    WRITE -.-> AUDIT_TRAIL
```

### State Report Format (filled example)

```
# Agent State Report — 2026-07-30 00:45:00

## Agent Identity
- Role: refinement-orchestrator
- Session: Hermes TUI, deepseek-v4-pro
- Last action: Completed all 109 refinement workers
- Time since last batch: <1 minute (pipeline complete)

## Pipeline Status
| Stage | Directory    | Expected | Actual | %    | Status |
|-------|-------------|----------|--------|------|--------|
| 1     | extracted/   | 109      | 109    | 100% | ✅     |
| 2     | refined/     | 109      | 109    | 100% | ✅     |
| 3     | merged/      | 2 files  | 2      | —    | ✅     |
| 4     | adapted/     | TBD      | 0      | —    | ⬜     |
| 5     | artifacts/   | 6        | 0      | —    | ⬜     |

## Errors & Blockers
| Sev | Description                                  | Action Needed            |
|-----|----------------------------------------------|--------------------------|
| 🔴  | 6 artifact files fabricated (pre-extraction) | Regenerate Stages 3→4→5  |
| 🟡  | PROGRESS.md was 31 batches behind            | Fixed; monitor going fwd |

## Rails Compliance
| Rail | Status | Issues Found |
|------|--------|-------------|
| R1   | PASS   | No cross-contamination |
| R2   | PASS   | rNNN-pPPPP-PPPP.md matches wNNN |
| R3   | PASS   | 109/109 verified on disk |
| R4   | PASS   | Zero content loss (10,927→21,852 lines) |
| R5   | PASS   | All 9 rules verified |
| R6   | PASS   | No fabrication detected |
| R7   | PASS   | REFINE-PROGRESS.md tracks all batches |
| R8   | PASS   | Slow workers completed without intervention |

## Files on Disk (verified, not claimed)
extracted/:  109 files, 912K  (10,927 lines)
refined/:    109 files, 916K  (21,852 lines)
merged/:       2 files, 708K  (master-raw.md, master.md)
adapted/:      0 files, 0B    (not started)
artifacts/:    0 files, 0B    (6 fabricated in root)
audit/:        4 files, 32K
prompts-refine/: 109 files, 436K
```

---

## 4. HANDOFF TRIGGERS — Stage Transition Signals

```mermaid
flowchart TD
    subgraph GATE0["GATE 0 — Pre-Flight"]
        G0A["✅ spec/issue-09-2025/ pages 1-434 exist"]
        G0B["✅ Directories: ste-code/extracted/ ste-code/prompts/"]
        G0C["✅ Worker grid: 109 workers, 37 batches mapped"]
    end

    subgraph GATE1["GATE 1 — Extraction → Refinement"]
        G1A["🔔 Signal: 109/109 extracted files on disk"]
        G1B["🔔 Signal: 10,927 lines across all files"]
        G1C["🔔 Signal: python3 check-rails.py — all 4 checks pass"]
        G1D["🔔 Signal: State report written to .hermes/audit/"]
        G1E["🔔 Signal: exchange.md turn: 'EXTRACTION COMPLETE'"]
    end

    subgraph GATE2["GATE 2 — Refinement → Continuation"]
        G2A["🔔 Signal: 109/109 refined files on disk"]
        G2B["🔔 Signal: 21,852 lines (format expansion, zero loss)"]
        G2C["🔔 Signal: All 9 refinement rules verified per rail R5"]
        G2D["🔔 Signal: No gaps in r001–r109"]
        G2E["🔔 Signal: State report written"]
        G2F["🔔 Signal: exchange.md turn: 'REFINEMENT COMPLETE'"]
    end

    subgraph GATE34["GATES 3-4 — Merge + Adapt"]
        G3A["🔔 Signal: master-raw.md (10,927L) + master.md exist"]
        G3B["🔔 Signal: 53 rules + 19 categories verified"]
        G3C["🔔 Signal: All 19 category-mapping entries populated"]
        G3D["🔔 Signal: Every adapted rule references master.md source"]
    end

    subgraph GATE5["GATE 5 — Artifacts"]
        G5A["🔔 Signal: 6 artifact files in ste-code/artifacts/"]
        G5B["🔔 Signal: Token budgets met per spec"]
        G5C["🔔 Signal: Anti-fabrication rules pass"]
        G5D["🔔 Signal: Final audit clean"]
    end

    GATE0 --> GATE1
    GATE1 --> GATE2
    GATE2 --> GATE34
    GATE34 --> GATE5

    G1A -.->|"Agent #1 writes exchange.md"| EX1["💬 Turn: Orchestrator → Reviewer<br/>'EXTRACTION PHASE COMPLETE'"]
    G2A -.->|"Agent #2 writes exchange.md"| EX2["💬 Turn: Refinement Orchestrator → Reviewer<br/>'REFINEMENT COMPLETE'"]
    G5A -.->|"Agent #4 writes exchange.md"| EX3["💬 Turn: Continuation Orchestrator → Reviewer<br/>'ALL ARTIFACTS GENERATED'"]
```

### Handoff Trigger Summary

| Transition | Who Finishes | Signal | Who Picks Up | Verification |
|-----------|-------------|--------|-------------|-------------|
| Gate 0 → 1 | User/Setup | Spec files exist | Agent #1 | `ls spec/issue-09-2025/page-*.md \| wc -l` = 434 |
| Gate 1 → 2 | Agent #1 | exchange.md: "EXTRACTION COMPLETE" | Agent #2 | 109 extracted files, 10,927 lines, check-rails.py passes |
| Gate 2 → 3 | Agent #2 | exchange.md: "REFINEMENT COMPLETE" | Agent #4 | 109 refined files, 21,852 lines, zero gaps, 9 rules verified |
| Gate 3 → 4 | Agent #4 | master.md validated | Agent #4 (same) | 53 rules, 19 categories, ~875 approved dict entries |
| Gate 4 → 5 | Agent #4 | All adapted files written | Agent #4 (same) | Every rule cross-references master.md source |
| Gate 5 → done | Agent #4 | exchange.md: artifacts complete | Reviewer | 6 files, token budgets met, anti-fab pass |

---

## 5. ERROR ESCALATION — Auditor Detection & Agent Response

```mermaid
flowchart TD
    AUDITOR["🔍 Agent #3 — Execution Auditor<br/>Runs continuously or on-demand<br/>'audit now', 'audit and fix'"]

    AUDITOR --> COLLECT["Step 1: Collect Claims<br/>Read PROGRESS.md, exchange.md,<br/>all SKILL.md progress logs"]
    COLLECT --> EVIDENCE["Step 2: Collect Evidence<br/>find/wc/stat on disk files<br/>(evidence-commands.md)")
    EVIDENCE --> XREF["Step 3: Cross-Reference<br/>For each claim:<br/>∃ file? >30 lines? timestamp? content?"]
    XREF --> FLAG["Step 4: Flag Discrepancies"]

    FLAG --> CRIT["🔴 CRITICAL<br/>- File claimed but missing<br/>- File empty/truncated<br/>- PROGRESS.md [x] but no file<br/>- Fabrication patterns detected"]
    FLAG --> ERR["🟠 ERROR<br/>- Wrong page range in file<br/>- Claimed count ≠ disk count<br/>- Stale tracking docs"]
    FLAG --> WARN["🟡 WARNING<br/>- File exists but not tracked<br/>- Retroactive claim timestamp<br/>- Multiple agents disagree"]

    CRIT --> FIXABLE{"Auto-fix<br/>safe?"}
    ERR --> FIXABLE
    WARN --> FIXABLE

    FIXABLE -->|"Yes (safe patterns)"| AUTOFIX["🛠️ Auto-Fix Applied<br/>- 22→19 category correction<br/>- deepseek-pro→v4-pro<br/>- Remove empty dirs<br/>- Delete fabricated artifacts<br/>- Sync PROGRESS.md with disk<br/>- Update stale README counts"]
    FIXABLE -->|"No (content issues)"| ESCALATE["🚨 Escalate to Agents<br/>Write to exchange.md<br/>Flag in audit report"]

    AUTOFIX --> RECHECK["♻️ Re-run audit to verify fix"]
    RECHECK --> REPORT["📋 Produce Audit Report<br/>.hermes/audit/audit-YYYYMMDD-HHMMSS.md<br/>Includes: claims ledger, evidence,<br/>discrepancies, auto-fixes, trust scores"]

    ESCALATE --> REPORT

    REPORT --> AGENTS["📢 All agents read audit report"]

    AGENTS --> A1RESP["Agent #1 Response<br/>- Re-launch failed workers<br/>- Split page range for truncated<br/>- Update PROGRESS.md"]
    AGENTS --> A2RESP["Agent #2 Response<br/>- Re-launch missing rNNN<br/>- Fix formatting violations<br/>- Update REFINE-PROGRESS.md"]
    AGENTS --> A3RESP["Agent #3 Response<br/>- Re-audit after fixes<br/>- Update trust scores<br/>- Verify no regression"]
    AGENTS --> A4RESP["Agent #4 Response<br/>- Replace fabricated artifacts<br/>- Cross-reference every claim<br/>- Re-verify anti-fab rules"]

    subgraph TRUST["📊 Agent Trust Scores (per audit)"]
        direction LR
        TS1["Extraction (execution): 100%<br/>Extraction (tracking): 0%"]
        TS2["Refinement (execution): 100%<br/>Refinement (tracking): 37%"]
        TS3["Auditor: 100%<br/>(3 audits, all verifiable)"]
    end

    REPORT -.-> TRUST

    subgraph FIXABLE_PATTERNS["🛠️ Safe Auto-Fix Patterns"]
        FP1["22→19 category count"]
        FP2["deepseek-pro→v4-pro model"]
        FP3["Empty stage directories"]
        FP4["Fabricated artifact files"]
        FP5["Stale PROGRESS.md counters"]
        FP6["README.md stale counts"]
    end

    subgraph UNFIXABLE["🚨 Escalate (Cannot Auto-Fix)"]
        UF1["Missing worker output → re-launch worker"]
        UF2["Truncated files → split page range, re-extract"]
        UF3["Fabricated content → delete, re-extract from spec"]
        UF4["Tracking lies → agent corrects own tracking"]
    end
```

### Error Escalation Protocol

| Severity | Detection Method | Who Flags | Fix Responsibility | Communication |
|----------|-----------------|-----------|-------------------|---------------|
| 🔴 CRITICAL | File missing, empty, or fabricated | Auditor | Originating agent re-launches worker | exchange.md + audit report |
| 🟠 ERROR | Wrong pages, stale tracking | Auditor | Auditor auto-fixes tracking; agent fixes content | exchange.md + audit report |
| 🟡 WARNING | Untracked work, timestamp issues | Auditor | Auditor auto-fixes safe patterns | Audit report only |
| 🟢 VERIFIED | All claims match disk evidence | Auditor | None needed | Trust score updated |

---

## 6. PARALLEL OPERATION — Concurrency Rules

```mermaid
flowchart TD
    subgraph CANNOT_OVERLAP["❌ CANNOT RUN SIMULTANEOUSLY"]
        direction TB
        X1["Stage 1 (Extract) ⇔ Stage 2 (Refine)<br/>Refinement reads from extracted/<br/>Must wait for extraction to finish<br/>Rail R1 violation otherwise"]
        X2["Stage 3 (Merge) ⇔ Stage 4 (Adapt)<br/>Adaptation reads from merged/<br/>Must wait for validated master.md"]
        X3["Stage 4 (Adapt) ⇔ Stage 5 (Artifacts)<br/>Artifacts read from adapted/<br/>Must wait for all adaptation complete"]
    end

    subgraph CAN_OVERLAP["✅ CAN RUN SIMULTANEOUSLY"]
        direction TB
        Y1["Auditor (#3) ⇔ ANY other agent<br/>Auditor reads files, never writes content<br/>Can audit extraction while refinement runs<br/>Can audit refinement while adaptation runs"]
        Y2["Within a stage: workers run in parallel<br/>Up to 3 workers per batch<br/>37 batches run sequentially<br/>(batch N+1 waits for batch N commit)"]
        Y3["Agent #4 Stages 3-4-5 run sequentially<br/>within the same agent session<br/>(merge → adapt → artifacts in order)"]
    end

    subgraph TIMING["⏱️ CONCURRENCY TIMELINE"]
        direction LR
        T0["t0: User launches<br/>Agent #1 (extract)"]
        T1["t1: Auditor checks<br/>while extraction runs"]
        T2["t2: Agent #1 complete<br/>→ signals exchange.md"]
        T3["t3: Agent #2 launches<br/>(refinement)"]
        T4["t4: Auditor checks<br/>while refinement runs"]
        T5["t5: Agent #2 complete<br/>→ signals exchange.md"]
        T6["t6: Agent #4 launches<br/>(merge→adapt→artifacts)"]
        T7["t7: Auditor final check<br/>while Agent #4 runs"]
    end

    CANNOT_OVERLAP --- CAN_OVERLAP --- TIMING
```

### Concurrency Matrix

|               | Agent #1<br/>(Extract) | Agent #2<br/>(Refine) | Agent #3<br/>(Auditor) | Agent #4<br/>(Continue) |
|---------------|:---:|:---:|:---:|:---:|
| **Agent #1**  | 3/batch | ❌ | ✅ | ❌ |
| **Agent #2**  | ❌ | 3/batch | ✅ | ❌ |
| **Agent #3**  | ✅ | ✅ | solo | ✅ |
| **Agent #4**  | ❌ | ❌ | ✅ | sequential |

Key:
- ❌ = Cannot overlap — must complete before other starts
- ✅ = Can overlap — safe to run simultaneously
- 3/batch = Stage-internal parallelism (3 workers, sequential batches)
- solo = One auditor instance at a time
- sequential = Stages 3→4→5 run in order within one agent

### Parallelism Rules

1. **Extraction + Refinement: MUTUALLY EXCLUSIVE.** Agent #2 reads `extracted/` output. If Agent #1 is still writing, Agent #2 would read incomplete data. Rail R1 (Stage Isolation) enforced.

2. **Auditor: ALWAYS PARALLEL-SAFE.** Agent #3 only reads files and writes immutable reports to `.hermes/audit/`. It never modifies content files. Auto-fixes only touch tracking docs and safe factual corrections. The auditor can run at any time without affecting active orchestrators.

3. **Within a stage: BATCHED PARALLELISM.** Each orchestrator launches 3 workers simultaneously, waits for all 3 to exit, verifies output, commits, then proceeds to next batch. Never more than 3 concurrent workers.

4. **Agent #4: SEQUENTIAL STAGES.** Merge → Adapt → Artifacts in strict order. Each stage gates on the previous stage's output being fully written and validated.

5. **Reviewer: ASYNCHRONOUS.** The user/reviewer can inspect `exchange.md` and audit reports at any time. The reviewer doesn't block agent progress but can inject corrections via `exchange.md` turns.

---

## Complete Communication Map

```mermaid
flowchart LR
    subgraph CHANNELS["📡 Communication Channels"]
        direction TB
        EX["💬 exchange.md<br/>Turn-based structured dialog<br/>Agents append, reviewer reads<br/>Stage completion signals"]
        AR["📋 Audit Reports<br/>audit-YYYYMMDD-HHMMSS.md<br/>Claims ledger vs evidence<br/>Trust scores, auto-fixes"]
        SR["📊 State Reports<br/>state-YYYYMMDD-HHMMSS.md<br/>8-section pipeline dashboard<br/>Triggered by 'state'/'report'"]
        PR["📈 Progress Trackers<br/>PROGRESS.md (extraction)<br/>REFINE-PROGRESS.md (refinement)<br/>Updated after every batch"]
    end

    subgraph AGENTS["🤖 Agents"]
        A1["Agent #1<br/>Extraction<br/>Orchestrator"]
        A2["Agent #2<br/>Refinement<br/>Orchestrator"]
        A3["Agent #3<br/>Execution<br/>Auditor"]
        A4["Agent #4<br/>Continuation<br/>Orchestrator"]
    end

    A1 -->|"writes completion"| EX
    A2 -->|"writes completion"| EX
    A3 -->|"writes findings + fixes"| EX
    A4 -->|"writes stage signals"| EX

    A1 -->|"updates every batch"| PR
    A2 -->|"updates every batch"| PR
    A3 -->|"auto-fixes when stale"| PR

    A1 -->|"on completion"| SR
    A2 -->|"on completion"| SR
    A3 -->|"produces per audit"| AR
    A3 -->|"on demand"| SR

    A3 -->|"reads all claims from"| EX
    A3 -->|"reads all claims from"| PR
    A3 -->|"cross-references all"| SR

    A2 -.->|"reads extraction complete"| EX
    A4 -.->|"reads refinement complete"| EX
    A4 -.->|"reads extracted/refined counts"| PR

    EX -.->|"reviewer injects corrections"| A1
    EX -.->|"reviewer injects corrections"| A2
    AR -.->|"all agents read for truth"| AGENTS

    classDef exchange fill:#e1f5fe,stroke:#0288d1
    classDef audit fill:#fff3e0,stroke:#f57c00
    classDef state fill:#e8f5e9,stroke:#388e3c
    classDef progress fill:#fce4ec,stroke:#c62828
    class EX exchange
    class AR audit
    class SR state
    class PR progress
```
