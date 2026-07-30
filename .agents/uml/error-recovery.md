# STE-Code Pipeline — Error Recovery & Edge Cases

> Authoritative troubleshooting reference. All diagrams use Mermaid.
> Cross-references: `rails.md`, `worker-rails.md`, `evidence-commands.md`, `worker-grid.md`, `SKILL.md` (execution-auditor).

---

## 1. FAILURE MODES — Complete Taxonomy

```mermaid
flowchart TD
    START["Worker Launched<br/>hermes -z '...' -m deepseek-v4-pro --yolo"] --> DISPATCH

    DISPATCH{"Dispatch<br/>Succeeded?"}
    DISPATCH -->|"Yes"| RUN["Worker Executes<br/>Reads 4 spec pages → writes .md"]
    DISPATCH -->|"No"| TO["TIMEOUT: Worker never starts<br/>Cause: deadlock, API unavailable"]

    RUN --> CHECK{"Output File<br/>Exists?"}
    CHECK -->|"Yes"| SIZE{"File Size > 3KB?<br/>> 30 lines?"}
    CHECK -->|"No"| CORRUPT["FILE CORRUPTION<br/>Worker crashed / disk full /<br/>hermes terminated mid-write"]

    SIZE -->|"Yes"| CONTENT{"Content<br/>Valid?"}
    SIZE -->|"No"| TRUNC["TRUNCATION<br/>Partial output:<br/>- Mid-word cutoff<br/>- Incomplete table<br/>- Missing closing content"]

    CONTENT -->|"Yes"| PASS["✅ Worker Succeeded"]
    CONTENT -->|"No"| FAB["FABRICATION<br/>- Modern SW terms in spec<br/>- Commentary language<br/>- Wrong page content<br/>- Missing ASD-STE100 boilerplate"]

    TO --> RECOVER1["RETRY: Re-launch worker<br/>with same params"]
    CORRUPT --> RECOVER2["RE-EXTRACT: Delete<br/>stale file, re-launch"]
    TRUNC --> RECOVER3["SPLIT: Halve page range<br/>(4 pages → 2+2)"]
    FAB --> RECOVER4["RE-EXTRACT: Delete<br/>fabricated file, re-launch<br/>from spec source"]

    style TO fill:#ff6b6b,stroke:#c92a2a,color:#000
    style CORRUPT fill:#ff6b6b,stroke:#c92a2a,color:#000
    style TRUNC fill:#ffa94d,stroke:#d9480f,color:#000
    style FAB fill:#ff6b6b,stroke:#c92a2a,color:#000
    style PASS fill:#51cf66,stroke:#2b8a3e,color:#000
```

### 1a. Shell Quoting Errors Detail

```mermaid
flowchart LR
    subgraph QUOTING["Shell Quoting Failures"]
        Q1["❌ Single-quote inside single-quote<br/>hermes -z 'Read page-0005.md's table'<br/>→ Shell parse error, never launched"]
        Q2["❌ Unescaped backticks<br/>hermes -z 'Write `code` blocks'<br/>→ Shell executes `code` as command"]
        Q3["❌ Newline in quoted string<br/>hermes -z 'line1\nline2'<br/>→ Truncated at backslash"]
        Q4["❌ Dollar-sign in prompt<br/>hermes -z 'Output $PATH'<br/>→ Shell expands variable"]
    end

    Q1 --> FIX_Q["FIX: Escape inner quotes with '\\''<br/>or use double-quote wrapper"]
    Q2 --> FIX_BT["FIX: Escape backticks with \\`<br/>or use heredoc"]
    Q3 --> FIX_NL["FIX: Use literal newlines in script<br/>not \\n escape sequences"]
    Q4 --> FIX_DS["FIX: Escape $ as \\$<br/>or use single-quoted heredoc delimiter"]

    style Q1 fill:#ff6b6b,stroke:#c92a2a,color:#000
    style Q2 fill:#ff6b6b,stroke:#c92a2a,color:#000
    style Q3 fill:#ffa94d,stroke:#d9480f,color:#000
    style Q4 fill:#ffa94d,stroke:#d9480f,color:#000
```

### 1b. Model Normalization Failure

```mermaid
flowchart TD
    REQ["Request: -m deepseek-v4-pro"] --> PROXY{"Hermes Proxy<br/>Model Router"}
    PROXY -->|"Normal"| OK["Routes to deepseek-v4-pro<br/>✅ Correct"]
    PROXY -->|"Misroute"| WRONG["Routes to deepseek-v4-flash<br/>❌ Wrong model"]
    PROXY -->|"Fallback"| FALLBACK["Model unavailable →<br/>falls back to cheaper model<br/>⚠️ Silent degradation"]

    WRONG --> DETECT1["DETECTION: Audit checks<br/>output for model-typical patterns:<br/>- 'deepseek-pro' in text<br/>- Unexpected formatting style"]
    FALLBACK --> DETECT2["DETECTION: Audit checks<br/>output quality signals:<br/>- Shorter than expected<br/>- Summarized instead of extracted"]

    DETECT1 --> FIX1["FIX: Patch model refs to<br/>deepseek-v4-pro, re-extract if<br/>content quality is degraded"]
    DETECT2 --> FIX2["FIX: Re-launch worker explicitly<br/>with -m deepseek-v4-pro flag"]

    style WRONG fill:#ff6b6b,stroke:#c92a2a,color:#000
    style FALLBACK fill:#ffa94d,stroke:#d9480f,color:#000
```

---

## 2. RECOVERY FLOWS — Per-Failure Response Matrix

### 2a. Batch-Level Recovery Decision Tree

```mermaid
flowchart TD
    BATCH["Batch N Launched<br/>3 workers in parallel"] --> WAIT["Wait for all 3 to finish<br/>(timeout: 120s per worker)"]

    WAIT --> RESULTS{"How Many<br/>Succeeded?"}

    RESULTS -->|"3/3 ✅"| VERIFY["VERIFY: Check all 3 files<br/>exist, >3KB, >30 lines,<br/>clean endings"]
    VERIFY --> PASS_ALL{"All Verified?"}
    PASS_ALL -->|"Yes"| COMMIT["git gcommit-hermes<br/>Update PROGRESS.md [x]<br/>Continue to Batch N+1"]
    PASS_ALL -->|"No"| FLAG["Flag specific worker<br/>for re-extraction"]

    RESULTS -->|"2/3"| PARTIAL["PARTIAL FAILURE<br/>1 worker failed"]
    RESULTS -->|"1/3"| MOST_FAIL["MOST FAILED<br/>2 workers failed"]
    RESULTS -->|"0/3"| ALL_FAIL["TOTAL FAILURE<br/>All 3 workers failed"]

    PARTIAL --> DIAG_PARTIAL["DIAGNOSE failed worker:<br/>- Check if file exists (empty?)<br/>- Check if timeout<br/>- Check if fabrication"]
    DIAG_PARTIAL --> RETRY{"Retry Strategy"}
    RETRY -->|"Timeout"| RELAUNCH["RE-LAUNCH: Same worker<br/>same page range, fresh session"]
    RETRY -->|"Truncation"| SPLIT_W["SPLIT: Divide 4 pages<br/>into 2+2, launch 2 workers"]
    RETRY -->|"Fabrication"| DEL_RELAUNCH["DELETE fabricated file<br/>RE-LAUNCH from spec source"]

    MOST_FAIL --> DIAG_MOST["DIAGNOSE root cause:<br/>- API outage?<br/>- Quoting error in batch?<br/>- Disk full?"]
    DIAG_MOST --> FIX_ROOT["FIX root cause first<br/>then re-launch ALL failed<br/>workers in this batch"]

    ALL_FAIL --> DIAG_ALL["DIAGNOSE systemic issue:<br/>- Check hermes proxy health<br/>- Check disk space<br/>- Check spec files readable<br/>- Check shell quoting"]
    DIAG_ALL --> FIX_SYSTEMIC["FIX systemic issue<br/>RE-LAUNCH entire batch"]

    RELAUNCH --> WAIT
    SPLIT_W --> WAIT
    DEL_RELAUNCH --> WAIT

    style COMMIT fill:#51cf66,stroke:#2b8a3e,color:#000
    style ALL_FAIL fill:#ff6b6b,stroke:#c92a2a,color:#000
    style MOST_FAIL fill:#ff6b6b,stroke:#c92a2a,color:#000
    style PARTIAL fill:#ffa94d,stroke:#d9480f,color:#000
```

### 2b. Split Strategy for Truncated Workers

```mermaid
flowchart LR
    TRUNC["Worker W042 truncated<br/>Original: pages 165-168<br/>Output: 18 lines, mid-word cutoff"] --> DELETE["rm ste-code/extracted/w042-p165-168.md"]

    DELETE --> SPLIT_A["Launch W042a<br/>pages 165-166<br/>→ w042a-p165-166.md"]
    DELETE --> SPLIT_B["Launch W042b<br/>pages 167-168<br/>→ w042b-p167-168.md"]

    SPLIT_A --> CHECK_A{"w042a OK?"}
    SPLIT_B --> CHECK_B{"w042b OK?"}

    CHECK_A -->|"Yes"| MERGE["MERGE: cat w042a w042b<br/>into w042-p165-168.md<br/>Add combined header"]
    CHECK_B -->|"Yes"| MERGE

    CHECK_A -->|"No"| SPLIT_AA["SPLIT AGAIN:<br/>pages 165 → w042a1<br/>pages 166 → w042a2"]
    CHECK_B -->|"No"| SPLIT_BB["SPLIT AGAIN:<br/>pages 167 → w042b1<br/>pages 168 → w042b2"]

    MERGE --> VERIFY_M["Verify merged file:<br/>> 30 lines, clean endings,<br/>correct page headers"]
    VERIFY_M --> DONE["✅ Mark batch complete"]

    style TRUNC fill:#ffa94d,stroke:#d9480f,color:#000
    style DONE fill:#51cf66,stroke:#2b8a3e,color:#000
```

---

## 3. AUDIT DETECTION — How the Auditor Finds Problems

### 3a. Full Audit Flow

```mermaid
flowchart TD
    TRIGGER["TRIGGER:<br/>- Batch claimed complete<br/>- Stage claimed complete<br/>- 'audit now' command"] --> COLLECT["Step 1: COLLECT CLAIMS<br/>Read PROGRESS.md [x] boxes<br/>Read feedback/exchange.md<br/>Build claims ledger"]

    COLLECT --> SWEEP["Step 2: EVIDENCE SWEEP<br/>count extracted/ files<br/>count refined/ files<br/>check file sizes & line counts<br/>check timestamps"]

    SWEEP --> XREF["Step 3: CROSS-REFERENCE<br/>For each claim:<br/>A. File exists?<br/>B. Content > 30 lines / > 3KB?<br/>C. Timestamp after claim?<br/>D. Content matches page range?<br/>E. Multiple agents consistent?"]

    XREF --> FLAGS{"Discrepancies<br/>Found?"}

    FLAGS -->|"No"| CLEAN["✅ AUDIT CLEAN<br/>Proceed to next gate"]
    FLAGS -->|"Yes"| CLASSIFY["CLASSIFY by severity:<br/>🔴 CRITICAL: file missing, fabricated,<br/>   PROGRESS.md lying<br/>🟠 ERROR: wrong pages, bad format<br/>🟡 WARNING: untracked work,<br/>   retroactive claims"]

    CLASSIFY --> REPORT["Step 5: AUDIT REPORT<br/>→ .agents/audit/audit-TIMESTAMP.md<br/>Includes: claims analyzed, evidence<br/>checked, discrepancies, trust scores,<br/>coverage map, recommendations"]

    REPORT --> FIX_CHECK{"Fixable<br/>Patterns?"}

    FIX_CHECK -->|"Yes"| AUTOFIX["AUTO-FIX: Apply safe fixes<br/>(22→19, model refs,<br/>remove empty dirs, delete<br/>fabricated artifacts)"]
    FIX_CHECK -->|"No"| ESCALATE["ESCALATE: Flag for<br/>agent intervention<br/>Re-extraction needed"]

    AUTOFIX --> REAUDIT["RE-AUDIT to confirm<br/>fixes applied correctly"]
    REAUDIT --> FINAL{"Clean?"}
    FINAL -->|"Yes"| CLEAN
    FINAL -->|"No"| ESCALATE

    style CLEAN fill:#51cf66,stroke:#2b8a3e,color:#000
    style FLAGS fill:#ffa94d,stroke:#d9480f,color:#000
    style ESCALATE fill:#ff6b6b,stroke:#c92a2a,color:#000
```

### 3b. Detection Methods Matrix

```mermaid
flowchart LR
    subgraph METHODS["Detection Methods"]
        direction TB
        M1["FILE COUNTS<br/>ls extracted/w*-p*.md | wc -l<br/>Expect: 109 files<br/>Actual vs expected gap"]
        M2["SIZE CHECKS<br/>for f in extracted/w*-p*.md<br/>  lines=$(wc -l < $f)<br/>  [ $lines -lt 30 ] → SUSPICIOUS<br/>  [ $lines -lt 80 ] → LIGHT"]
        M3["GAP DETECTION<br/>for pg in $(seq 1 434)<br/>  grep -rq page-$pg extracted/<br/>  missing pages accumulate"]
        M4["FABRICATION SWEEP<br/>grep -rl 'React\|Docker\|npm' extracted/<br/>grep -rl 'This page describes' extracted/<br/>grep -L 'ASD-STE100' extracted/"]
        M5["TIMESTAMP AUDIT<br/>PROGRESS.md mod time<br/>vs extracted/ file mod times<br/>→ claim after file = retroactive"]
        M6["DUPLICATE CHECK<br/>diff w001-p1-4.md w042-p165-168.md<br/>→ identical output = fabrication"]
    end

    M1 --> SEV1["🔴 CRITICAL"]
    M2 --> SEV2["🔴 CRITICAL if < 30<br/>🟡 WARNING if 30-79"]
    M3 --> SEV3["🔴 CRITICAL<br/>Uncovered pages"]
    M4 --> SEV4["🔴 CRITICAL<br/>Fabricated content"]
    M5 --> SEV5["🟡 WARNING<br/>Retroactive claim"]
    M6 --> SEV6["🔴 CRITICAL<br/>Duplicate fabrication"]

    style M1 fill:#e3f2fd,stroke:#1565c0
    style M2 fill:#e3f2fd,stroke:#1565c0
    style M3 fill:#e3f2fd,stroke:#1565c0
    style M4 fill:#e3f2fd,stroke:#1565c0
    style M5 fill:#e3f2fd,stroke:#1565c0
    style M6 fill:#e3f2fd,stroke:#1565c0
```

---

## 4. AUTO-FIXES vs AGENT INTERVENTION

```mermaid
flowchart TD
    FINDING["Audit Finding"] --> CAN_I{"Can Auditor<br/>Fix This?"}

    CAN_I -->|"YES — Safe"| AUTO["AUTO-FIX QUEUE"]
    CAN_I -->|"NO — Requires Agent"| ESCALATE["ESCALATION QUEUE"]

    subgraph AUTO_FIXES["SAFE AUTO-FIXES (Auditor executes)"]
        AF1["22 → 19 category count<br/>patch all files"]
        AF2["deepseek-pro → deepseek-v4-pro<br/>patch all model references"]
        AF3["hermes -z file I/O false claim<br/>patch to corrected text"]
        AF4["Empty ste-code/extracted/<br/>rm -rf the empty directory"]
        AF5["Fabricated artifact files<br/>(6 .txt + PLAN.md + README.md)<br/>rm individual files"]
        AF6["Stale ste-code/prompts/<br/>rm -rf entire directory"]
        AF7["Wrong naming convention<br/>mv to correct pattern"]
    end

    subgraph ESCALATIONS["AGENT INTERVENTION REQUIRED"]
        E1["Missing worker output files<br/>Workers must re-extract"]
        E2["Truncated worker files<br/>Split page range, re-extract"]
        E3["Fabricated worker content<br/>Delete, re-extract from spec"]
        E4["PROGRESS.md tracking errors<br/>Agent corrects own tracking"]
        E5["Stage isolation violations<br/>Move files to correct stage dir"]
        E6["Content fidelity failures<br/>Re-extract/refine from source"]
    end

    AF1 --> REAUDIT1["Re-audit → confirm"]
    AF2 --> REAUDIT1
    AF3 --> REAUDIT1
    AF4 --> REAUDIT1
    AF5 --> REAUDIT1
    AF6 --> REAUDIT1
    AF7 --> REAUDIT1

    REAUDIT1 --> LOG1["Log in audit report<br/>under ## Auto-Fixes Applied"]

    style AUTO_FIXES fill:#e8f5e9,stroke:#2b8a3e
    style ESCALATIONS fill:#fff3e0,stroke:#d9480f
```

---

## 5. RAILS VIOLATIONS — Detection & Recovery

```mermaid
flowchart TD
    subgraph RAILS["8 Process Rails — Violation Detection & Recovery"]
        direction TB

        R1["RAIL 1: STAGE ISOLATION"]
        R1 --> R1D["DETECT: File in wrong stage dir<br/>e.g. refined/ written during extraction"]
        R1 --> R1R["RECOVER: Move file to _scratch/<br/>Regenerate in correct stage"]

        R2["RAIL 2: NAMING CONVENTION"]
        R2 --> R2D["DETECT: File doesn't match pattern<br/>wNNN-pPPPP-PPPP.md or rNNN-pPPPP-PPPP.md"]
        R2 --> R2R["RECOVER: mv to correct name<br/>Auto-fixable by auditor"]

        R3["RAIL 3: COMPLETION INTEGRITY"]
        R3 --> R3D["DETECT: [x] in PROGRESS.md but<br/>file missing, empty, or truncated"]
        R3 --> R3R["RECOVER: Revert [x] → [ ]/<br/>Re-extract missing files<br/>Verify ALL 3 before marking [x]"]

        R4["RAIL 4: CONTENT FIDELITY"]
        R4 --> R4D["DETECT: Fabrication signals —<br/>modern terms, commentary,<br/>missing boilerplate, wrong facts"]
        R4 --> R4R["RECOVER: Delete fabricated file<br/>Re-extract from spec source<br/>Auto-fix: 22→19, model refs"]

        R5["RAIL 5: FORMATTING STANDARDS"]
        R5 --> R5D["DETECT: Glued headings,<br/>no blank line after tables,<br/>wrong STE/Non-STE format"]
        R5 --> R5R["RECOVER: Re-refine with<br/>formatting rules enforced<br/>Auto-fix: patch glued headings"]

        R6["RAIL 6: FACTUAL CORRECTNESS"]
        R6 --> R6D["DETECT: '22 categories',<br/>'deepseek-pro',<br/>'hermes -z no file I/O'"]
        R6 --> R6R["RECOVER: patch to correct facts<br/>19 categories / deepseek-v4-pro<br/>Auto-fixable by auditor"]

        R7["RAIL 7: PROGRESS TRACKING"]
        R7 --> R7D["DETECT: [x] without verification<br/>[!] never used for failures<br/>Timestamps missing"]
        R7 --> R7R["RECOVER: Correct PROGRESS.md<br/>Update after verification<br/>Use [!] for failed workers"]

        R8["RAIL 8: ERROR RECOVERY"]
        R8 --> R8D["DETECT: Mistake ignored, hidden,<br/>or papered over with false claim"]
        R8 --> R8R["RECOVER: Acknowledge the error<br/>Apply the specific fix for that<br/>error type (see above rows)"]
    end

    style R1 fill:#e3f2fd,stroke:#1565c0
    style R2 fill:#e3f2fd,stroke:#1565c0
    style R3 fill:#e3f2fd,stroke:#1565c0
    style R4 fill:#e3f2fd,stroke:#1565c0
    style R5 fill:#e3f2fd,stroke:#1565c0
    style R6 fill:#e3f2fd,stroke:#1565c0
    style R7 fill:#e3f2fd,stroke:#1565c0
    style R8 fill:#e3f2fd,stroke:#1565c0
```

### 5b. Worker Rails (W1-W10) Violation Recovery

```mermaid
flowchart TD
    subgraph W_RAILS["Worker Rails Detection (W1-W10) — Self-Validated"]
        W1["W1: Missing '# Page N of M' header"] --> W1F["FIX: Insert header from page range"]
        W2["W2: Glued headings (no blank line)"] --> W2F["FIX: Insert blank line after ###/####"]
        W3["W3: Fabrication (commentary/modern terms)"] --> W3F["FIX: Delete file, re-extract from spec"]
        W4["W4: Boilerplate repeated on every line"] --> W4F["FIX: Re-extract with boilerplate control"]
        W5["W5: Wrong STE/Non-STE format"] --> W5F["FIX: Reformat to > **STE:** / > **Non-STE:**"]
        W6["W6: Broken tables (missing separators)"] --> W6F["FIX: Re-extract page with table focus"]
        W7["W7: No blank line after tables"] --> W7F["FIX: Insert blank line after each table"]
        W8["W8: Triple+ blank lines"] --> W8F["FIX: Collapse to max 2 blank lines"]
        W9["W9: Content incomplete (omissions)"] --> W9F["FIX: Re-extract with explicit completeness instruction"]
        W10["W10: Wrong filename pattern"] --> W10F["FIX: mv to correct pattern (auto-fixable)"]
    end

    W1F --> VERIFY["Re-verify after fix:<br/>wc -l, grep glued, head -1"]
    VERIFY --> RETRY_W{"Pass?"}
    RETRY_W -->|"Yes"| DONE_W["✅ Worker complete"]
    RETRY_W -->|"No"| SPLIT_W["Split page range,<br/>re-launch narrower worker"]

    style W1 fill:#fff3e0,stroke:#d9480f
    style W2 fill:#fff3e0,stroke:#d9480f
    style W3 fill:#ffebee,stroke:#c92a2a
    style W4 fill:#fff3e0,stroke:#d9480f
    style W5 fill:#fff3e0,stroke:#d9480f
    style W6 fill:#fff3e0,stroke:#d9480f
    style W7 fill:#fff3e0,stroke:#d9480f
    style W8 fill:#fff3e0,stroke:#d9480f
    style W9 fill:#ffebee,stroke:#c92a2a
    style W10 fill:#e8f5e9,stroke:#2b8a3e
```

---

## 6. BATCH RESTART — Complete Mid-Pipeline Recovery

```mermaid
stateDiagram-v2
    [*] --> Healthy: Pipeline running

    state "Pipeline State Machine" as PS {
        Healthy --> BatchN: Launch Batch N

        BatchN --> VerifyBatch: All 3 workers finished
        VerifyBatch --> BatchPass: 3/3 verified ✅
        VerifyBatch --> BatchPartial: 1-2/3 failed
        VerifyBatch --> BatchFail: 3/3 failed

        BatchPass --> CommitBatch: git gcommit-hermes
        CommitBatch --> Healthy: Continue to Batch N+1

        BatchPartial --> DiagnosePartial
        DiagnosePartial --> RetryFailed: Retry failed workers (same range)
        DiagnosePartial --> SplitFailed: Split truncated workers (2+2)
        DiagnosePartial --> ReextractFailed: Re-extract fabricated

        RetryFailed --> VerifyBatch
        SplitFailed --> VerifyBatch
        ReextractFailed --> VerifyBatch

        BatchFail --> DiagnoseFull
        DiagnoseFull --> FixSystemic: Fix root cause
        FixSystemic --> BatchN: Re-launch entire batch
    }

    state "Batch Restart Recovery" as BR {
        [*] --> IdentifyLastGood: Read PROGRESS.md for last [x] batch

        IdentifyLastGood --> VerifyLastGood: Audit last good batch on disk
        VerifyLastGood --> NextBatch: Calculate next batch number (last_good + 1)

        NextBatch --> UpdateProgress: Revert any false [x] to [ ] for batches > last_good
        UpdateProgress --> Resume: Launch Batch (last_good + 1)

        Resume --> PS: Resume pipeline from checkpoint
    }

    state "Full Restart Decision" as FR {
        [*] --> AssessDamage: Run Execution Auditor — full audit
        AssessDamage --> Decision{Extraction % complete?}

        Decision --> Continue: > 80% — resume from last good batch
        Decision --> PartialRedo: 30-80% — audit, fix, resume
        Decision --> FullRedo: < 30% — rm -rf extracted/ refined/ merged/, restart from Batch 1

        Continue --> BR
        PartialRedo --> BR
        FullRedo --> FreshStart: Reset PROGRESS.md, re-init directories
        FreshStart --> PS: Start from Batch 1
    }
```

### 6a. Restart Decision Tree

```mermaid
flowchart TD
    INTERRUPT["Pipeline Interrupted<br/>Mid-Extraction"] --> AUDIT["RUN: Execution Auditor<br/>Full audit of claims vs disk"]

    AUDIT --> COVERAGE["Calculate Coverage:<br/>verified pages / 434"]

    COVERAGE --> DECISION{"Coverage %"}

    DECISION -->|"> 90%"| RESUME["RESUME: Find last<br/>complete batch in PROGRESS.md<br/>Launch Batch N+1<br/>Verify existing files intact"]
    DECISION -->|"50-90%"| AUDIT_FIX["AUDIT+FIX: Run auditor<br/>in fix mode. Delete stale/fab.<br/>Re-extract missing pages.<br/>Resume from first gap."]
    DECISION -->|"< 50%"| NUKE["NUKE: rm -rf extracted/<br/>rm -rf refined/ merged/<br/>Reset PROGRESS.md to empty<br/>Re-init directories<br/>START FROM BATCH 1"]

    RESUME --> CHECK_EXISTING["Verify existing files:<br/>for batch in 1..N:<br/>  all 3 files exist and valid"]
    CHECK_EXISTING -->|"All good"| LAUNCH_N1["Launch Batch N+1"]
    CHECK_EXISTING -->|"Some missing"| FILL_GAPS["Fill gaps: re-extract<br/>specific missing workers<br/>then continue"]

    AUDIT_FIX --> FIX_RESUME["Fix what's fixable<br/>Re-extract what's not<br/>Rebuild claims ledger<br/>Resume from first gap"]

    NUKE --> INIT["Re-init stage directories<br/>Reset PROGRESS.md<br/>git gcommit-hermes"]
    INIT --> BATCH1["Launch Batch 1"]

    LAUNCH_N1 --> CONTINUE["Continue pipeline<br/>normally from checkpoint"]
    FILL_GAPS --> CONTINUE

    style RESUME fill:#51cf66,stroke:#2b8a3e,color:#000
    style NUKE fill:#ff6b6b,stroke:#c92a2a,color:#000
    style AUDIT_FIX fill:#ffa94d,stroke:#d9480f,color:#000
```

### 6b. PROGRESS.md State During Restart

```mermaid
flowchart LR
    subgraph BEFORE["PROGRESS.md — Before Restart"]
        B1["Batch 15: [x] ✅"]
        B2["Batch 16: [x] ✅"]
        B3["Batch 17: [x] ❌ (false claim)"]
        B4["Batch 18: [ ]"]
        B5["Batch 19: [ ]"]
    end

    subgraph AUDIT["Auditor Cross-References"]
        A1["Check disk: Batch 16 files exist"]
        A2["Check disk: Batch 17 files MISSING"]
    end

    subgraph AFTER["PROGRESS.md — After Fix"]
        C1["Batch 15: [x] ✅"]
        C2["Batch 16: [x] ✅"]
        C3["Batch 17: [ ] ← REVERTED"]
        C4["Batch 18: [ ]"]
        C5["Batch 19: [ ]"]
    end

    B2 --> A1
    B3 --> A2
    A2 --> C3

    style B3 fill:#ff6b6b,stroke:#c92a2a,color:#000
    style C3 fill:#ffa94d,stroke:#d9480f,color:#000
```

---

## 7. GIT RECOVERY — Commit Failures & Sync Conflicts

```mermaid
flowchart TD
    subgraph GIT_FLOW["Git Recovery Flow"]
        COMMIT["git gcommit-hermes<br/>after Batch N verified"] --> STATUS{"Commit<br/>Succeeded?"}

        STATUS -->|"Yes"| PUSH["git push origin Current"]
        STATUS -->|"No"| DIAG_GIT["DIAGNOSE:<br/>- Unstaged changes?<br/>- Merge conflict?<br/>- Detached HEAD?<br/>- Pre-commit hook fail?"]

        PUSH --> PUSH_STATUS{"Push<br/>Succeeded?"}
        PUSH_STATUS -->|"Yes"| DONE_GIT["✅ Git synced"]
        PUSH_STATUS -->|"No"| SYNC_ISSUE["SYNC CONFLICT:<br/>Remote has diverged"]

        DIAG_GIT --> UNSTAGED{"Unstaged<br/>Changes?"}
        UNSTAGED -->|"Yes"| STAGE["git add ste-code/extracted/ .agents/state/<br/>Retry gcommit-hermes"]
        UNSTAGED -->|"No"| CONFLICT{"Merge<br/>Conflict?"}

        CONFLICT -->|"Yes"| RESOLVE["RESOLVE:<br/>1. Backup current state<br/>2. git stash<br/>3. git pull --rebase<br/>4. git stash pop<br/>5. Resolve conflicts in .agents/<br/>6. Retry gcommit-hermes"]
        CONFLICT -->|"No"| DETACHED{"Detached<br/>HEAD?"}

        DETACHED -->|"Yes"| REATTACH["git checkout Current<br/>Cherry-pick orphaned commits<br/>Retry gcommit-hermes"]
        DETACHED -->|"No"| HOOK_FAIL{"Pre-commit<br/>Hook Fail?"}

        HOOK_FAIL -->|"Yes"| FIX_HOOK["Fix hook issue<br/>(lint, test, format)<br/>Retry gcommit-hermes<br/>or git commit --no-verify"]
        HOOK_FAIL -->|"No"| MANUAL["Manual investigation<br/>git status, git log --oneline -5<br/>Resolve and retry"]

        SYNC_ISSUE --> PULL_FIRST["1. git fetch origin<br/>2. git rebase origin/Current<br/>3. Resolve any conflicts<br/>4. git push origin Current"]
    end

    STAGE --> COMMIT
    RESOLVE --> COMMIT
    REATTACH --> COMMIT
    FIX_HOOK --> COMMIT
    MANUAL --> COMMIT
    PULL_FIRST --> PUSH

    style DONE_GIT fill:#51cf66,stroke:#2b8a3e,color:#000
    style SYNC_ISSUE fill:#ffa94d,stroke:#d9480f,color:#000
    style CONFLICT fill:#ff6b6b,stroke:#c92a2a,color:#000
```

### 7a. Git State After Partial Commit Failure

```mermaid
stateDiagram-v2
    [*] --> PreCommit: Batch N verified, ready to commit

    PreCommit --> Staged: git add extracted/ state/
    Staged --> Committed: git gcommit-hermes succeeds
    Staged --> FailedCommit: git gcommit-hermes fails

    Committed --> Pushed: git push succeeds
    Committed --> PushFailed: git push fails (remote ahead)

    FailedCommit --> Diagnose: Check git status
    Diagnose --> FixAndRetry: Resolve issue, retry commit
    FixAndRetry --> Staged

    PushFailed --> Rebase: git rebase origin/Current
    Rebase --> RebaseConflict: Conflict in .agents/state/PROGRESS.md
    Rebase --> RebaseOK: Rebase clean
    RebaseConflict --> ResolveConflict: Manual merge PROGRESS.md
    ResolveConflict --> RebaseOK
    RebaseOK --> Pushed

    Pushed --> [*]: Batch N complete in git
```

### 7b. Emergency Recovery: Lost Commits

```mermaid
flowchart TD
    PANIC["PANIC: git log shows<br/>missing commits after<br/>failed rebase/merge"] --> REFLOG["CHECK REFLOG:<br/>git reflog --oneline -20<br/>Find lost commit hashes"]

    REFLOG --> FOUND{"Found lost<br/>commits?"}
    FOUND -->|"Yes"| RECOVER["RECOVER:<br/>git cherry-pick <hash><br/>or git reset --hard <hash><br/>or git branch recovery <hash>"]
    FOUND -->|"No"| FS_CHECK["FILESYSTEM CHECK:<br/>Are the extracted/ files<br/>still on disk?"]

    FS_CHECK --> FILES_OK{"Files on<br/>disk?"}
    FILES_OK -->|"Yes"| RECOMMIT["RE-COMMIT:<br/>git add -A ste-code/extracted/<br/>git add .agents/state/<br/>git gcommit-hermes<br/>This creates new commits but<br/>preserves the work"]
    FILES_OK -->|"No"| DISASTER["DISASTER: Both commits<br/>AND files are lost.<br/>Must re-extract from spec.<br/>Start from Batch 1."]

    RECOVER --> VERIFY_RECOVERY["Verify: git log --oneline -5<br/>Confirm all batches accounted for"]
    RECOMMIT --> VERIFY_RECOVERY
    VERIFY_RECOVERY --> DONE["✅ Recovery complete"]

    style DISASTER fill:#ff6b6b,stroke:#c92a2a,color:#000
    style DONE fill:#51cf66,stroke:#2b8a3e,color:#000
    style PANIC fill:#ff6b6b,stroke:#c92a2a,color:#000
```

---

## 8. COMPLETE TROUBLESHOOTING STATE MACHINE

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Launching: Batch N triggered

    Launching --> Running: Workers dispatched (3 parallel)
    Launching --> DispatchError: Shell quoting error / API unavailable

    Running --> Verifying: All workers reported done
    Running --> PartialFailure: 1-2 workers timed out/crashed
    Running --> TotalFailure: All 3 workers failed

    DispatchError --> FixQuoting: Escape special chars
    FixQuoting --> Launching: Retry dispatch

    Verifying --> AuditCheck: Run execution auditor
    AuditCheck --> BatchOK: All files valid, PROGRESS.md updated
    AuditCheck --> AuditFlagged: Discrepancies found

    AuditFlagged --> AutoFix: Safe patterns detected
    AuditFlagged --> AgentFix: Requires re-extraction

    AutoFix --> AuditCheck: Re-audit after fixes
    AgentFix --> Running: Re-launch specific workers

    PartialFailure --> DiagnoseFailed: Check file sizes, error patterns
    DiagnoseFailed --> SplitWorker: Truncated → split page range
    DiagnoseFailed --> RetryWorker: Timeout → re-launch same range
    DiagnoseFailed --> ReextractWorker: Fabricated → delete + re-extract

    SplitWorker --> Running: Launch split workers
    RetryWorker --> Running: Re-launch worker
    ReextractWorker --> Running: Re-launch worker

    TotalFailure --> DiagnoseSystemic: Check API health, disk, shell quoting
    DiagnoseSystemic --> FixSystemicIssue: Resolve root cause
    FixSystemicIssue --> Launching: Re-launch full batch

    BatchOK --> CommitGit: git gcommit-hermes
    CommitGit --> CommitOK: Commit succeeded
    CommitGit --> CommitFail: Commit failed

    CommitOK --> PushGit: git push
    PushGit --> PushOK: Push succeeded
    PushGit --> PushFail: Push rejected

    CommitFail --> FixGit: Diagnose + fix git state
    FixGit --> CommitGit: Retry commit

    PushFail --> RebaseGit: git rebase origin/Current
    RebaseGit --> PushGit: Retry push

    PushOK --> Idle: Ready for Batch N+1
    CommitOK --> Idle: Ready for Batch N+1 (local only)
```

---

## Appendix A: Severity Classification Reference

```mermaid
flowchart LR
    subgraph SEVERITY["Discrepancy Severity"]
        direction TB
        C1["🔴 CRITICAL<br/>Action: STOP pipeline"]
        C2["🟠 ERROR<br/>Action: Fix before continuing"]
        C3["🟡 WARNING<br/>Action: Note, continue"]

        C1 --> C1_EX["File claimed but missing<br/>File exists but empty/truncated<br/>PROGRESS.md [x] but no file<br/>Fabricated content detected<br/>Duplicate worker output<br/>Content fidelity violation"]
        C2 --> C2_EX["Claimed page range wrong<br/>Formatting standards violated<br/>Wrong naming convention<br/>Files in wrong stage dir"]
        C3 --> C3_EX["Work done but not tracked<br/>Claim timestamp after file timestamp<br/>Multiple agents claim different states<br/>File > 3KB but < 80 lines"]
    end

    style C1 fill:#ff6b6b,stroke:#c92a2a,color:#000
    style C2 fill:#ffa94d,stroke:#d9480f,color:#000
    style C3 fill:#ffd43b,stroke:#fab005,color:#000
```

---

## Appendix B: Quick Recovery Command Reference

```mermaid
flowchart TD
    subgraph CMDS["Emergency Recovery Commands"]
        CMD1["🔍 Full Audit<br/>hermes -z 'Read execution-auditor SKILL.md.<br/>Audit all claims vs disk evidence.<br/>Report to .agents/audit/audit-NOW.md'<br/>-m deepseek-v4-pro --yolo"]
        CMD2["🔧 Audit + Fix<br/>hermes -z 'Read execution-auditor SKILL.md.<br/>Full audit + apply all safe auto-fixes.<br/>Report to .agents/audit/audit-NOW.md'<br/>-m deepseek-v4-pro --yolo"]
        CMD3["📊 Coverage Check<br/>for pg in $(seq 1 434); do<br/>  grep -rq page-$(printf '%04d' $pg) ste-code/extracted/ || echo missing $pg<br/>done"]
        CMD4["🗑️  Emergency Clean<br/>rm -rf ste-code/extracted/w*-p*.md<br/>rm -rf ste-code/refined/r*-p*.md<br/>Reset PROGRESS.md to Batch 1<br/>(Only if < 30% coverage)"]
        CMD5["🔄 Resume Pipeline<br/>Read PROGRESS.md for last [x] batch.<br/>Launch Batch (last_batch + 1)<br/>Continue pipeline normally"]
        CMD6["💾 Git Rescue<br/>git reflog --oneline -20<br/>git cherry-pick &lt;lost-hash&gt;<br/>Or: git add -A && git gcommit-hermes"]
    end

    style CMD4 fill:#ff6b6b,stroke:#c92a2a,color:#000
    style CMD1 fill:#e3f2fd,stroke:#1565c0
    style CMD2 fill:#e8f5e9,stroke:#2b8a3e
    style CMD3 fill:#e3f2fd,stroke:#1565c0
    style CMD5 fill:#e8f5e9,stroke:#2b8a3e
    style CMD6 fill:#fff3e0,stroke:#d9480f
```

---

## Appendix C: Auditor Trust Score Calculation

```mermaid
flowchart LR
    CLAIMS["Total Claims<br/>= PROGRESS.md [x] count<br/>+ explicit claims in feedback"] --> CALC

    VERIFIED["Verified Claims<br/>= claims where:<br/>- File exists<br/>- File > 30 lines<br/>- Timestamp consistent<br/>- Content matches range"] --> CALC

    CALC["trust = verified / total"] --> SCORE{"Trust Score"}

    SCORE -->|"1.00"| A["✅ PERFECT<br/>Proceed to next gate"]
    SCORE -->|"0.80-0.99"| B["🟡 GOOD<br/>Investigate gaps, continue"]
    SCORE -->|"0.50-0.79"| C["🟠 POOR<br/>Fix before continuing"]
    SCORE -->|"< 0.50"| D["🔴 BROKEN<br/>Full audit and restart"]

    style A fill:#51cf66,stroke:#2b8a3e,color:#000
    style B fill:#ffd43b,stroke:#fab005,color:#000
    style C fill:#ffa94d,stroke:#d9480f,color:#000
    style D fill:#ff6b6b,stroke:#c92a2a,color:#000
```
