# Worker Lifecycle — Mermaid Diagrams

> Source documents:
> - `.agents/skills/ste-code-workers/SKILL.md`
> - `.agents/skills/references/worker-grid.md`
> - `.agents/skills/references/rails.md`
> - `.agents/skills/references/worker-rails.md`
> - `.agents/prompts/agent-1-extractor.md`

---

## Version History

| Version | Sections Added | Trigger |
|---------|---------------|---------|
| v1 | Section 1 (Worker Launch Sequence): launch command template, flag table | Initial pipeline design |
| v2 | Section 2 (Batch Protocol): 3-worker cycles, 6-item quality checklist; Section 4 (Polling Loop): coordinator-side flowchart | Truncation issues found during extraction |
| v3 | Section 3 (Worker States): state diagram and transition table; Section 5 (Error Recovery): error recovery matrix, Execution Auditor integration | Fabrication detected in worker output; v2 to v3 protocol correction from `agent-communication.md` applied to Polling Loop |

---

## 1. WORKER LAUNCH SEQUENCE

```mermaid
flowchart TD
    A["Coordinator: determine page range\n(e.g. pages 1–4)"] --> B["Generate worker ID\nW001, page range 1-4"]
    B --> C["Write prompt file to disk\nste-code/prompts/w001-prompt.txt"]
    C --> D{"Prompt file written\nsuccessfully?"}
    D -- NO --> D1["Retry: ensure directory exists,\nrewrite prompt"]
    D1 --> C
    D -- YES --> E["LAUNCH: hermes -z\nbackground=true\nnotify_on_complete=true"]
    E --> F["hermes -z reads prompt\nvia $(cat prompt.txt)"]
    F --> G["Worker reads source spec pages\nspec/issue-09-2025/page-0001.md\nthrough page-0004.md"]
    G --> H["Worker extracts ALL content\n— no summarization\n— every word, table, example"]
    H --> I["Worker self-validates\nagainst 10 Worker Rails\n(W1–W10)"]
    I --> J["Worker writes output\nste-code/extracted/w001-p1-4.md"]
    J --> K["hermes -z process exits\n→ notify_on_complete fires"]
    K --> L["Coordinator receives\nnotification: worker done"]

    style E fill:#4a9,stroke:#333,color:#fff
    style K fill:#49a,stroke:#333,color:#fff
```

### Launch Command Template

```
hermes -z "$(cat ste-code/prompts/wNNN-prompt.txt)" -m deepseek-v4-pro --yolo
```

**Flags:**
| Flag | Meaning |
|------|---------|
| `-z` | One-shot mode: execute prompt, write output, exit |
| `-m deepseek-v4-pro` | Model selection (RAIL 6: immutable) |
| `--yolo` | Skip confirmation prompts for file writes |
| `background=true` | Launched via Hermes terminal with bg tracking |
| `notify_on_complete=true` | Coordinator gets automatic exit notification |

**Critical constraint:** Prompt is always written to a file and passed via `$(cat …)`. Never embed multi-line prompts directly in the shell command — shell quoting breaks.

---

## 2. BATCH PROTOCOL (3-Worker Cycles)

```mermaid
flowchart TD
    subgraph BATCH["BATCH N (3 workers)"]
        direction LR
        W1["WRITE prompt\n→ wNNN-prompt.txt"] --> L1["LAUNCH W_X\nbg + notify"]
        W2["WRITE prompt\n→ wMMM-prompt.txt"] --> L2["LAUNCH W_Y\nbg + notify"]
        W3["WRITE prompt\n→ wPPP-prompt.txt"] --> L3["LAUNCH W_Z\nbg + notify"]
    end

    BATCH --> WAIT["WAIT for all 3\nnotify_on_complete signals"]
    WAIT --> V1{"File exists?\ntest -f"}
    V1 -- NO --> FAIL1["🔴 CRITICAL\nWorker failed silently"]
    V1 -- YES --> V2{"Size > 3KB?\n>30 lines?"}
    V2 -- NO --> FAIL2["🟠 ERROR\nEmpty or truncated"]
    V2 -- YES --> V3{"Last 3 lines\nend cleanly?"}
    V3 -- NO --> FAIL3["🟠 ERROR\nTruncation detected"]
    V3 -- YES --> V4{"Content signals\npresent?"}
    V4 -- NO --> FAIL4["🟡 WARNING\nWrong content?"]
    V4 -- YES --> V5{"Fabrication\ncheck pass?"}
    V5 -- NO --> FAIL5["🔴 CRITICAL\nFabricated content"]
    V5 -- YES --> PASS["✅ All 3 workers\nverified"]

    FAIL1 --> RECOVER
    FAIL2 --> RECOVER
    FAIL3 --> RECOVER
    FAIL4 --> RECOVER
    FAIL5 --> RECOVER

    RECOVER["ERROR RECOVERY\nSplit page range in half\nRe-extract both halves"] --> BATCH

    PASS --> COMMIT["git add -A\n\ngit gcommit-hermes\n'Batch N: workers W_X–W_Z\n(pages A–B)'"]
    COMMIT --> TRACK["Update .agents/state/PROGRESS.md\nFlip [ ] → [x] for all 3 workers\nUpdate progress counter"]
    TRACK --> NEXT{"More batches\nremaining?"}
    NEXT -- YES --> BATCH
    NEXT -- NO --> DONE["🎉 ALL 109 WORKERS\nCOMPLETE\n(37 batches, 434 pages)"]
```

### Per-Batch Quality Checklist (6-item gate)

| # | Check | Command / Signal |
|---|-------|-----------------|
| 1 | Output files exist | `test -f ste-code/extracted/wNNN-pPPPP-PPPP.md` |
| 2 | Size > 3KB | `wc -l` must report > 30 lines for 4-page extraction |
| 3 | No truncation | Last 3 lines end cleanly (period, footer, or table row) — not mid-word, not partial `\|` |
| 4 | Content signals | "ASD-STE100 Simplified Technical English" header, "Issue 9" / "2025-01-15" footers present |
| 5 | No fabrication | No modern terms ("React", "Docker"), no commentary ("This page describes…"), reads like a spec |
| 6 | Tracking updated | `grep "\[x\]" .agents/state/PROGRESS.md \| wc -l` matches completed workers |

---

## 3. WORKER STATES

```mermaid
stateDiagram-v2
    [*] --> idle : Coordinator selects\npage range

    idle --> prompt_written : Write prompt file\nto ste-code/prompts/

    prompt_written --> running : hermes -z launch\nbackground=true\nnotify_on_complete=true

    state running {
        [*] --> reading_source : Read spec pages\nfrom spec/issue-09-2025/
        reading_source --> extracting : Parse markdown
        extracting --> self_validating : Apply Worker Rails\n(W1–W10)
        self_validating --> writing_output : Write to\nste-code/extracted/
        writing_output --> [*] : process exits
    }

    running --> exited_success : Exit code 0\nOutput file written
    running --> exited_failure : Exit code ≠ 0\nor no output file
    running --> exited_timeout : Exceeded time limit\n(~60s per worker)

    exited_success --> verifying : Coordinator runs\n6-item quality checklist
    exited_failure --> recovery : Split page range\nre-extract
    exited_timeout --> recovery : Split page range\nre-extract

    state verifying {
        [*] --> check_file : File exists?
        check_file --> check_size : Size > 3KB?
        check_size --> check_truncation : Last 3 lines clean?
        check_truncation --> check_signals : Content signals?
        check_signals --> check_fabrication : Fabrication check?
        check_fabrication --> [*] : All 3 workers pass
        --
        check_file --> check_failed : Missing
        check_size --> check_failed : Too small
        check_truncation --> check_failed : Truncated
        check_signals --> check_failed : Wrong content
        check_fabrication --> check_failed : Fabricated
    }

    check_failed --> recovery : Split page range\nre-extract

    verifying --> verified : All 6 checks pass\nfor all 3 workers
    recovery --> idle : Re-launch with\nhalved page ranges

    verified --> committed : git gcommit-hermes\nUpdate PROGRESS.md
    committed --> [*] : Worker state finalized\nImmutable on disk

    note right of committed
        Once committed, worker output
        is immutable. The Execution
        Auditor may later verify it
        but never modifies it.
    end note

    note right of recovery
        Recovery rule (RAIL 8):
        Split the failed worker's
        4-page range into two
        2-page ranges and
        re-extract both.
    end note
```

### State Transition Table

| From | To | Trigger | Action |
|------|----|---------|--------|
| `idle` | `prompt_written` | Coordinator selects page range | Write prompt to `ste-code/prompts/wNNN-prompt.txt` |
| `prompt_written` | `running` | `hermes -z` launched with bg+notify | Process starts, reads source pages |
| `running` | `exited_success` | Worker exits with code 0 | Output file exists on disk |
| `running` | `exited_failure` | Worker exits with code ≠ 0 | No output file, or file is empty |
| `running` | `exited_timeout` | Process exceeds ~60s limit | Worker may be stuck or processing too many pages |
| `exited_success` | `verifying` | notify_on_complete signals coordinator | Run 6-item quality checklist |
| `exited_failure` | `recovery` | Automatic on failure | Split page range, re-extract |
| `exited_timeout` | `recovery` | Automatic on timeout | Split page range, re-extract |
| `verifying` | `verified` | All 6 checks pass | Ready for commit |
| `verifying` | `recovery` | Any check fails | Split page range, re-extract |
| `verified` | `committed` | Batch complete (all 3 verified) | `git gcommit-hermes`, update PROGRESS.md |
| `committed` | `[*]` | Terminal state | File is immutable on disk |

---

## 4. POLLING LOOP (Coordinator-Side)

```mermaid
flowchart TD
    START["START BATCH\nN = current batch number"] --> GEN["Generate 3 prompts\nWrite to ste-code/prompts/"]
    GEN --> LAUNCH["Launch 3 workers\nterminal(background=true,\nnotify_on_complete=true)"]
    LAUNCH --> WAIT["Wait for notifications\nAll 3 notify_on_complete\nsignals received"]

    WAIT --> POLL["POLL: collect exit statuses\nprocess(action='poll')"]

    POLL --> CHK1{"All 3 output\nfiles exist?"}
    CHK1 -- NO --> REC1["Mark missing workers [!]\nIdentify failed range"]
    CHK1 -- YES --> CHK2{"All sizes\n> 3KB?"}
    CHK2 -- NO --> REC2["Mark undersized [!]\nFlag for split"]
    CHK2 -- YES --> CHK3{"Last 3 lines\nall clean?"}

    CHK3 -->|"mid-word end?"| REC3A["Truncation: split range"]
    CHK3 -->|"partial | row?"| REC3B["Truncation: split range"]
    CHK3 -->|"all clean"| CHK4{"Content signals\npresent?"}

    CHK4 -- NO --> REC4["Check section-types.md\nRe-extract with correct range"]
    CHK4 -- YES --> CHK5{"Fabrication\ncheck pass?"}

    CHK5 -->|"modern terms found"| REC5A["🔴 Delete file\nRe-extract from spec"]
    CHK5 -->|"commentary found"| REC5B["🔴 Delete file\nRe-extract from spec"]
    CHK5 -->|"all clean"| PASS["✅ Batch N verified"]

    REC1 --> SPLIT
    REC2 --> SPLIT
    REC3A --> SPLIT
    REC3B --> SPLIT
    REC4 --> SPLIT
    REC5A --> SPLIT
    REC5B --> SPLIT

    SPLIT["SPLIT RECOVERY\nDivide 4-page range →\ntwo 2-page ranges"] --> RETRY["Generate new prompts\nfor split ranges\nRe-launch workers"]
    RETRY --> WAIT

    PASS --> COMMIT["COMMIT\n1. git add -A\n2. git gcommit-hermes 'Batch N'\n3. Update PROGRESS.md\n   Flip [ ] → [x]\n   Update counter"]
    COMMIT --> AUDIT{"Execution Auditor\nauto-audit?"}
    AUDIT -- YES --> AUDIT_RUN["Auditor cross-references\nPROGRESS.md vs disk\n4-step protocol"]
    AUDIT_RUN --> AUDIT_OK{"Discrepancies?"}
    AUDIT_OK -- YES --> AUDIT_FIX["Auto-fix safe patterns\nFlag unfixable"]
    AUDIT_OK -- NO --> NEXT
    AUDIT -- NO --> NEXT

    NEXT{"Batch N+1\n≤ 37?"}
    NEXT -- YES --> START
    NEXT -- NO --> FINAL["FINAL AUDIT\npython3 ste-code/check-rails.py\n4 checks must pass\n→ Write state report\n→ Signal in exchange.md"]
```

### Poll System Protocol (from agent-1-extractor.md)

```
WRITE prompt to file
  → LAUNCH: hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo (background + notify_on_complete=true)
  → WAIT for all 3 in batch to exit
  → VERIFY: output file exists, size >3KB, no truncation
  → COMMIT: git add -A && git gcommit-hermes
  → NEXT batch
```

**Key constraints:**
- Never launch more than 3 at once
- Never skip verification
- Never commit before all 3 pass all 6 checks
- Never proceed to next batch with [!] marks in PROGRESS.md

---

## 5. ERROR RECOVERY

```mermaid
flowchart TD
    ERR["ERROR DETECTED\nduring verification"] --> CLASSIFY{"Classify error type"}

    CLASSIFY -->|"Worker timeout\n(>60s no output)"| TO["TIMEOUT RECOVERY"]
    CLASSIFY -->|"Shell quoting failure\n(prompt mangled)"| SQ["QUOTING RECOVERY"]
    CLASSIFY -->|"Model normalization\n(wrong model used)"| MN["MODEL RECOVERY"]
    CLASSIFY -->|"Truncation detected\n(mid-word / partial row)"| TR["TRUNCATION RECOVERY"]
    CLASSIFY -->|"Fabrication detected\n(commentary / modern terms)"| FB["FABRICATION RECOVERY"]
    CLASSIFY -->|"File missing\n(worker exited ≠ 0)"| FM["MISSING FILE RECOVERY"]
    CLASSIFY -->|"Undersized output\n(<3KB, <30 lines)"| US["UNDERSIZED RECOVERY"]

    TO --> SPLIT["Split page range in half\n4 pages → two 2-page ranges"]
    SQ --> REWRITE["Rewrite prompt to file\nUse $(cat file) pattern\nNever embed multi-line in shell"]
    MN --> CORRECT["Ensure -m deepseek-v4-pro\n(RAIL 6: immutable model)\nRe-launch with correct model"]
    TR --> SPLIT
    FB --> DELETE["Delete fabricated file\nrm ste-code/extracted/wNNN-*.md"]
    FM --> SPLIT
    US --> SPLIT

    SPLIT --> GEN_NEW["Generate 2 replacement prompts\nwNNNa-prompt.txt (first half)\nwNNNb-prompt.txt (second half)"]
    REWRITE --> RELAUNCH["Re-launch worker\nwith corrected prompt"]
    CORRECT --> RELAUNCH
    DELETE --> GEN_ORIG["Re-generate original prompt\nfor the same page range"]
    GEN_ORIG --> RELAUNCH
    GEN_NEW --> RELAUNCH

    RELAUNCH --> RECHECK["Re-verify after re-launch\nRun 6-item checklist again"]
    RECHECK -->|"PASS"| MARK["Mark [!] → [x] in PROGRESS.md\nContinue batch protocol"]
    RECHECK -->|"FAIL AGAIN"| ESCALATE["🟠 ESCALATE\nLog in .agents/feedback/exchange.md\nFlag for Execution Auditor review\nTry once more with single-page ranges"]
```

### Error Recovery Matrix (RAIL 8)

| Error | Detection Signal | Root Cause | Recovery Action | Retry Limit |
|-------|-----------------|------------|-----------------|-------------|
| **Worker Timeout** | No notify_on_complete after ~60s | Too many pages, model stalled | Split 4-page range into two 2-page ranges | 2 → escalate |
| **Shell Quoting Failure** | Prompt garbled, model misinterprets | Multi-line prompt in shell command | Rewrite prompt to file, use `$(cat file)` | 1 (fix is reliable) |
| **Model Normalization** | Wrong model in launch command | `deepseek-pro` or `deepseek-v4-flash` used | Correct to `deepseek-v4-pro` (RAIL 6) | 1 (fix is reliable) |
| **Truncation** | Last line ends mid-word, partial table row, missing footer | Model output limit, page count too high | Split page range in half; re-extract both halves | 2 → single pages |
| **Fabrication** | Modern terms ("React", "Docker"), commentary ("This page describes..."), narrative prose | Model hallucinating instead of extracting | Delete file; re-extract from spec with stricter prompt | 2 → flag for manual review |
| **Missing File** | `test -f` returns false, worker exited ≠ 0 | Worker crashed, disk full, path error | Verify directory exists; split range; re-launch | 2 → skip and flag |
| **Undersized** | < 3KB or < 30 lines for 4 pages | Worker extracted too little, early exit | Split range; re-extract | 2 → single pages |

### Anti-Fabrication Rules (appended to every worker prompt)

All worker prompts include these immutable constraints:
- Output contains ONLY text from the spec pages
- No commentary ("This page describes...", "The key point is...")
- No modern terms not in the spec ("React", "Docker", "API")
- No summarization — every word, table, example
- Every file starts with `# Page N of M`
- Output filename must match `wNNN-pPPPP-PPPP.md`

### Execution Auditor Integration

```mermaid
flowchart LR
    BATCH["Batch N\nverified ✅"] --> AUDIT_TRIGGER{"Auto-audit\nenabled?"}
    AUDIT_TRIGGER -- YES --> AUDIT["Execution Auditor\n4-step protocol"]
    AUDIT_TRIGGER -- NO --> NEXT["Next batch"]

    AUDIT --> COLLECT["Step 1: Collect claims\nRead PROGRESS.md,\nexchange.md, agent messages"]
    COLLECT --> EVIDENCE["Step 2: Collect evidence\nCheck file existence,\nsize, content, timestamps"]
    EVIDENCE --> XREF["Step 3: Cross-reference\n5 questions per claim"]
    XREF --> FLAG["Step 4: Flag discrepancies\n🔴 Critical / 🟠 Error / 🟡 Warning"]

    FLAG --> FIXABLE{"Fixable\npatterns?"}
    FIXABLE -->|"22→19, model refs,\nempty dirs"| AUTO_FIX["Auto-fix safe patterns\nvia patch / terminal"]
    FIXABLE -->|"Missing files,\ntruncated content"| REPORT["Flag only\nCannot auto-fix\n(content generation)"]

    AUTO_FIX --> REPORT_WRITE["Write audit report\n.agents/audit/audit-*.md\nImmutable, append-only"]
    REPORT --> REPORT_WRITE
    REPORT_WRITE --> NEXT
```

---

## 6. KNOWN LIMITATIONS

### Worker Hang Beyond Timeout

If a worker does not exit after the 60s timeout and `notify_on_complete` does not fire, the coordinator blocks indefinitely. The current protocol has no deadman timer. The operator must manually check `process(action='list')` and kill stuck workers.

### Git Commit Failure Mid-Batch

If `git gcommit-hermes` fails (merge conflict, pre-commit hook failure, or authentication error), the batch is in a partial state. PROGRESS.md may show `[x]` but the commit did not land. Recovery: re-run `git gcommit-hermes` after fixing the root cause. If the commit succeeded but PROGRESS.md update failed, update PROGRESS.md manually and continue.

### Filesystem Full During Extraction

If the disk is full, worker output files are truncated or empty. The 6-item checklist catches undersized files but cannot recover without freeing space. The coordinator must stop all batches, free disk space, and re-launch failed workers.

### Overlapping Page Range Conflicts

If two coordinators run at the same time or page range assignments overlap, workers overwrite each other's output files. The output from the second worker replaces the first. This causes silent data loss. Prevent this with a PID lock file in `ste-code/.coordinator-lock`.

### Prompt Directory Deleted Mid-Run

If the `ste-code/prompts/` directory is deleted while workers run, already-launched workers are not affected. New worker launches fail because the prompt file does not exist. Recovery: recreate the directory and regenerate prompt files from the worker grid.

### Notification Signal Loss

If the Hermes runtime crashes between worker exit and `notify_on_complete` delivery, the coordinator never learns the worker finished. The process enters a silent deadlock. The operator must check `process(action='poll')` on all worker sessions and manually advance the batch.

### Maximum Retry Depth Exhausted

If a single-page extraction (after two splits of a 4-page range) still fails, the protocol has no further fallback. The page range is flagged for manual review. The coordinator records the failure in exchange.md and continues with the next batch.

---

## Summary: End-to-End Worker Lifecycle

```mermaid
flowchart TD
    subgraph PHASE1["PHASE 1: LAUNCH"]
        A1["1. Select page range (4 pages)"] --> A2["2. Write prompt to file"]
        A2 --> A3["3. hermes -z launch\nbg + notify_on_complete"]
    end

    subgraph PHASE2["PHASE 2: EXECUTION"]
        B1["4. Worker reads source pages"] --> B2["5. Worker extracts content"]
        B2 --> B3["6. Worker self-validates\n(10 Worker Rails)"]
        B3 --> B4["7. Worker writes output file"]
    end

    subgraph PHASE3["PHASE 3: VERIFICATION"]
        C1["8. notify_on_complete fires"] --> C2["9. Coordinator polls exit status"]
        C2 --> C3["10. Run 6-item quality checklist"]
        C3 --> C4{"All checks\npass?"}
        C4 -- YES --> C5["11. Mark verified ✅"]
        C4 -- NO --> C6["12. Error recovery\nSplit range → re-extract"]
        C6 --> A1
    end

    subgraph PHASE4["PHASE 4: COMMIT"]
        D1["13. All 3 workers in batch verified"] --> D2["14. git add -A"]
        D2 --> D3["15. git gcommit-hermes"]
        D3 --> D4["16. Update PROGRESS.md\nFlip [ ] → [x]"]
    end

    subgraph PHASE5["PHASE 5: AUDIT"]
        E1["17. Execution Auditor runs\n(if auto-audit enabled)"] --> E2["18. Cross-reference claims vs disk"]
        E2 --> E3["19. Auto-fix safe patterns\nFlag unfixable discrepancies"]
    end

    PHASE1 --> PHASE2
    PHASE2 --> PHASE3
    C5 --> PHASE4
    PHASE4 --> PHASE5
    PHASE5 --> NEXT_BATCH["Next batch\n(or DONE if batch 37)"]

    style A3 fill:#4a9,stroke:#333,color:#fff
    style B4 fill:#49a,stroke:#333,color:#fff
    style C5 fill:#2a2,stroke:#333,color:#fff
    style D4 fill:#a92,stroke:#333,color:#fff
```

**Scale numbers:**
- 434 source pages ÷ 4 pages per worker = **109 workers**
- 109 workers ÷ 3 per batch = **37 batches**
- ~30–60 seconds per worker → **~20–37 minutes** total extraction time
- 6 verification checks per batch, 8 error recovery patterns, 10 worker rails

---

## Meta-Instructions for Self-Rewriting

Use these instructions to update this document.

### Add a New Error Class

1. Add the new error class to the Error Recovery flowchart (Section 5). Use the pattern: `CLASSIFY -->|"description"| CODE["RECOVERY NAME"]`.
2. Add a row to the Error Recovery Matrix. Fill all 5 columns: Error, Detection Signal, Root Cause, Recovery Action, Retry Limit.
3. Add a recovery path node to the Polling Loop flowchart (Section 4). Connect the new error to the SPLIT node.
4. If the new error class introduces a new verification check, add it to the Per-Batch Quality Checklist (Section 2).
5. Run Quality Gate G2: verify the error class count in the flowchart equals the matrix row count.

### Update Retry Limits

1. Find the error class row in the Error Recovery Matrix.
2. Change the Retry Limit value.
3. Update the ESCALATE path description in the Error Recovery flowchart if the limit changes the fallback behavior.
4. Run Quality Gate G3: verify the row has all 5 columns filled.

### Add a New Verification Check

1. Add a numbered row to the Per-Batch Quality Checklist (Section 2). Use the next available number.
2. Add a check node to the Batch Protocol flowchart (Section 2). Use the pattern: `V{N}{"Description"}`.
3. Add a check state to the verifying substate in the Worker States diagram (Section 3). Use the pattern: `check_new --> [*]` for the pass path.
4. Add a check branch to the Polling Loop flowchart (Section 4). Use the pattern: `CHK{N}{"Description"}`.
5. Update the state transition table: add rows for the new check pass and fail transitions.
6. Run Quality Gate G5: verify the checklist item count equals the V-node count in the flowchart.

### Remove a Deprecated Error Class

1. Remove the error class branch from the Error Recovery flowchart.
2. Remove the row from the Error Recovery Matrix.
3. Remove the recovery path node from the Polling Loop flowchart.
4. Run Quality Gates G2 and G3.

### General Rules

- Use the STE-Code synonym table for all procedural text.
- Use American English spelling.
- Keep each procedural sentence at 20 words or fewer.
- Keep each descriptive sentence at 25 words or fewer.
- Do not use contractions.
- Do not use "-ing" forms as main verbs in procedures.

---

## Measurable Quality Gates

This document must pass these quality gates after each update.

| Gate | Rule | Check Method |
|------|------|-------------|
| G1 | State diagram node count (Section 3) must equal transition table row count | Count states in the `stateDiagram-v2` block. Count rows in the transition table. The two counts must be equal. |
| G2 | Every error class in the Error Recovery flowchart must have a matching row in the Error Recovery Matrix | Count `CLASSIFY -->|` branches in the flowchart. Count rows in the matrix. The two counts must be equal. |
| G3 | Every error class row must have all 5 columns: Detection Signal, Root Cause, Recovery Action, Retry Limit | Scan matrix rows. Flag rows with empty cells. No row may have missing columns. |
| G4 | Every diagram section must have a corresponding table or list summary | Verify each ` ```mermaid ` block is followed by a table or bullet list within 20 lines. Flag sections that have no summary. |
| G5 | Checklist item count (Section 2) must equal verification check nodes in the Batch Protocol flowchart | Count checklist rows. Count V-nodes in the flowchart. The two counts must be equal. |
| G6 | No unapproved words outside of code nouns | Run `ste-code/check-rails.py` on this document. The script must report 0 violations. |

---

## Agentic-Load Specifications

Processors that load this document can use this load map to optimize token use.

### Critical Sections (load first, ~150 lines)

| Section | Lines (approx.) | Value | Use |
|---------|-----------------|-------|-----|
| 3. Worker States | 65 | Highest value for understanding | The state diagram and transition table are the authoritative reference for all worker behavior. Load this first. |
| 4. Polling Loop | 70 | Highest value for execution | The coordinator-side flowchart is the step-by-step protocol for running batches. Load this when operating the pipeline. |

### Reference Sections (load on demand, ~180 lines)

| Section | Lines (approx.) | Value | Use |
|---------|-----------------|-------|-----|
| 1. Worker Launch Sequence | 40 | Reference | The exact launch command and flag meanings. Load only when you debug launch failures. |
| 2. Batch Protocol | 50 | Reference | The 3-worker cycle and 6-item checklist. Load when you design new batch workflows. |
| 5. Error Recovery | 90 | Reference only | The matrix tells you which recovery action to take. Load only when a worker fails. |

### Metadata Sections (load for auditing, ~120 lines)

| Section | Lines (approx.) | Value | Use |
|---------|-----------------|-------|-----|
| Version History | 10 | Audit trail | Shows which sections were revised and when. Load before auditing document changes. |
| Known Limitations | 30 | Operational awareness | Required reading before running the pipeline at scale. Load once before batch operations. |
| Meta-Instructions | 40 | Contributor guidance | Required for contributors who modify this document. Load before editing. |
| Quality Gates | 20 | Compliance check | Run after each document update. Load after editing. |

### Summary Section (~50 lines)

| Section | Lines (approx.) | Value | Use |
|---------|-----------------|-------|-----|
| End-to-End Summary | 50 | Quick recall | A compressed version of the full lifecycle. Good for quick recall. Not sufficient for execution. |

### Load Strategy

For first-time understanding, load in this order: Section 3, Section 4, End-to-End Summary, Known Limitations. Total: ~215 lines. For execution, load Section 4 and Known Limitations. Total: ~100 lines. For debugging a failed worker, load Section 5 and Version History. Total: ~100 lines.
