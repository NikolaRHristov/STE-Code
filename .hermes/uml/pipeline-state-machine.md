# STE-Code Pipeline — Master State Machine Blueprint

> **Source:** ASD-STE100 Issue 9, January 2025 (434 pages)
> **Agents:** Extraction (#1), Refinement (#2), Auditor (#3), Continuation (#4)
> **Model:** deepseek-v4-pro exclusively
> **Key Facts:** 53 writing rules + 4 GR rules, 19 technical noun categories, ~875 approved + ~1400 unapproved dictionary entries

---

## 1. High-Level Pipeline Flow

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Gate0_VerifySpec

    state "Agent #1\nExtraction Orchestrator" as A1
    state "Agent #2\nRefinement Orchestrator" as A2
    state "Agent #4 (Stages 3-5)\nContinuation Orchestrator" as A4
    state "Agent #3 (cross-cutting)\nExecution Auditor" as A3

    Gate0_VerifySpec --> Stage1_Extract : GATE 0 ✅
    Stage1_Extract --> Gate1_Verify : GATE 1
    Gate1_Verify --> Stage2_Refine : GATE 1 ✅
    Stage2_Refine --> Gate2_Verify : GATE 2
    Gate2_Verify --> Stage3_Merge : GATE 2 ✅
    Stage3_Merge --> Gate3_Verify : GATE 3
    Gate3_Verify --> Stage4_Adapt : GATE 3 ✅
    Stage4_Adapt --> Gate4_Verify : GATE 4
    Gate4_Verify --> Stage5_Artifacts : GATE 4 ✅
    Stage5_Artifacts --> [*] : PIPELINE COMPLETE

    note right of A1 : 109 workers\n37 batches of 3\n434 pages → 109 files
    note right of A2 : 109 workers\n37 batches of 3\n9 refinement rules
    note right of A4 : Merge → Adapt → Artifacts\nSingle threaded, sequential
    note left of A3 : Real-time disk verification\nCross-references all claims\nR1-R8 rail enforcement

    A3 --> Stage1_Extract : audits
    A3 --> Stage2_Refine : audits
    A3 --> Stage3_Merge : audits
    A3 --> Stage4_Adapt : audits
    A3 --> Stage5_Artifacts : audits

    Gate0_VerifySpec --> AuditFail : GATE 0 ❌
    Gate1_Verify --> AuditFail : GATE 1 ❌
    Gate2_Verify --> AuditFail : GATE 2 ❌
    Gate3_Verify --> AuditFail : GATE 3 ❌
    Gate4_Verify --> AuditFail : GATE 4 ❌
    AuditFail --> Gate0_VerifySpec : fix & retry
```

---

## 2. Stage 1 — Extraction (Agent #1)

```mermaid
stateDiagram-v2
    [*] --> Gate0 : ENTRY
    Gate0 --> Gate0_SpecCheck : Verify spec paths exist
    Gate0_SpecCheck --> Gate0_Setup : GATE 0 ✅
    Gate0_SpecCheck --> Gate0_Fail : paths missing
    Gate0_Fail --> Gate0_SpecCheck : fix paths

    Gate0_Setup --> BatchLoop

    state BatchLoop {
        [*] --> GeneratePrompts : write 3 prompts to disk
        GeneratePrompts --> LaunchWorkers : hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo
        LaunchWorkers --> WorkerRun : 3 workers parallel (bg + notify_on_complete)
        WorkerRun --> WaitAll : wait for all 3 to exit
        WaitAll --> VerifyBatch : verify output files
        VerifyBatch --> CommitBatch : git add -A && git gcommit-hermes
        CommitBatch --> UpdateProgress : update PROGRESS.md
        UpdateProgress --> CheckComplete : all 109 workers done?
        CheckComplete --> GeneratePrompts : next batch (37 total)
        CheckComplete --> BatchDone : YES → all 109 done

        state WorkerRun {
            [*] --> W1 : WNNN (pages A-B)
            [*] --> W2 : WNNN (pages C-D)
            [*] --> W3 : WNNN (pages E-F)

            W1 --> W1_Exit : output → extracted/
            W2 --> W2_Exit : output → extracted/
            W3 --> W3_Exit : output → extracted/
        }

        state VerifyBatch {
            [*] --> SizeCheck : file size > 3KB?
            SizeCheck --> SizePass : YES
            SizeCheck --> SizeFail : NO → flag
            SizePass --> NoTrunc : no truncation markers?
            NoTrunc --> VerifyOK : YES
            NoTrunc --> TruncFail : NO → flag
        }
    }

    BatchDone --> Gate1

    state Gate1 {
        [*] --> G1_Count : ls ste-code/extracted/w*-p*.md | wc -l → 109
        G1_Count --> G1_ZeroByte : find -size 0 → empty
        G1_ZeroByte --> G1_Gaps : iterate 1-109, all present
        G1_Gaps --> G1_Rails : python3 ste-code/check-rails.py
        G1_Rails --> G1_Quality : spot-check 3 random files
        G1_Quality --> G1_Pass : ALL CHECKS PASS
        G1_Quality --> G1_Fail : any check fails
    }

    G1_Pass --> Gate1_Signal : signal in exchange.md
    Gate1_Signal --> Stage2_Entry : HANDOFF to Agent #2
    G1_Fail --> BatchLoop : re-launch failed workers
```

---

## 3. Stage 2 — Refinement (Agent #2)

```mermaid
stateDiagram-v2
    [*] --> Gate1_Verify : ENTRY (from Stage 1)
    Gate1_Verify --> VerifyInput : 109 files in extracted/
    VerifyInput --> Gate1_Precheck : all > 3KB, no gaps

    Gate1_Precheck --> Setup : mkdir -p ste-code/refined .hermes/prompts/refine
    Setup --> BatchLoop

    state BatchLoop {
        [*] --> GeneratePrompts : write 3 full prompts (no abbreviation)
        GeneratePrompts --> LaunchWorkers : hermes -z "$(cat .hermes/prompts/refine/rNNN-prompt.txt)" -m deepseek-v4-pro --yolo
        LaunchWorkers --> WorkerRun : 3 workers parallel (bg + notify_on_complete)
        WorkerRun --> WaitAll : wait for all 3 to exit
        WaitAll --> VerifyBatch : verify output files
        VerifyBatch --> CommitBatch : git add && git commit "Batch N"
        CommitBatch --> UpdateProgress : update REFINE-PROGRESS.md + exchange.md every 10
        UpdateProgress --> CheckComplete : all 109 workers done?
        CheckComplete --> GeneratePrompts : next batch (37 total)
        CheckComplete --> BatchDone : YES → all 109 done

        state WorkerRun {
            [*] --> R1 : rNNN (pages A-B)
            [*] --> R2 : rNNN (pages C-D)
            [*] --> R3 : rNNN (pages E-F)

            R1 --> R1_Exit : output → refined/
            R2 --> R2_Exit : output → refined/
            R3 --> R3_Exit : output → refined/
        }

        state VerifyBatch {
            [*] --> SizeCheck : file size > 3KB?
            SizeCheck --> SizePass : YES
            SizeCheck --> RecoverMissing : NO → check disk (may have written before hang)
            RecoverMissing --> SplitAndRetry : still missing → split page range in half
            SizePass --> RuleCheck : 9 refinement rules applied?
            RuleCheck --> OmissionCheck : grep for "..." omissions?
            OmissionCheck --> OmissionFound : YES → mark FAILED, re-launch stronger
            OmissionCheck --> VerifyOK : NO → passes
        }
    }

    BatchDone --> Gate2

    state Gate2 {
        [*] --> G2_Count : ls ste-code/refined/r*-p*.md | wc -l → 109
        G2_Count --> G2_ZeroByte : find ste-code/refined -size 0 → empty
        G2_ZeroByte --> G2_Gaps : iterate r001-r109, all present
        G2_Gaps --> G2_Rails : python3 .hermes/scripts/check-rails.py
        G2_Rails --> G2_SpotCheck : spot-check 3 random files (formatting, no "...")
        G2_SpotCheck --> G2_Pass : ALL CHECKS PASS
        G2_SpotCheck --> G2_Fail : any check fails
    }

    G2_Pass --> Gate2_Signal : signal in exchange.md + state report
    Gate2_Signal --> Stage3_Entry : HANDOFF to Agent #4
    G2_Fail --> BatchLoop : re-launch failed workers
```

---

## 4. Stage 3 — Merge (Agent #4, first phase)

```mermaid
stateDiagram-v2
    [*] --> Gate2_Verify : ENTRY (from Stage 2)
    Gate2_Verify --> VerifyInput : 109 files in refined/

    VerifyInput --> ReadAll : read r001 through r109 in page order
    ReadAll --> Concatenate : concat into merged/master-raw.md
    Concatenate --> Deduplicate : remove repeated rule statements, categories, dictionary entries at page boundaries
    Deduplicate --> Organize : organize by section

    state Organize {
        [*] --> FrontMatter : Front matter
        FrontMatter --> Part1 : Part 1 — Rules 1.1–9.4 + GR1–GR4
        Part1 --> Categories : 19 technical noun categories
        Categories --> Part2 : Part 2 — Dictionary A–Z
        Part2 --> Appendices : Appendices
        Appendices --> WriteMaster : write merged/master.md
    }

    WriteMaster --> Gate3

    state Gate3 {
        [*] --> G3_Rules : grep -c "^#### Rule" master.md → 53
        G3_Rules --> G3_Categories : verify 19 categories present
        G3_Categories --> G3_DictApproved : count APPROVED entries → ~875
        G3_DictApproved --> G3_DictUnapproved : count UNAPPROVED entries → ~1400
        G3_DictUnapproved --> G3_SpotCheck : spot-check 10 random pages vs original spec
        G3_SpotCheck --> G3_Pass : ALL CHECKS PASS
        G3_SpotCheck --> G3_Fail : any check fails
    }

    G3_Pass --> Gate3_Signal : signal in exchange.md
    Gate3_Signal --> Stage4_Entry : PROCEED to Adaptation
    G3_Fail --> ReadAll : redo merge from refined files
```

---

## 5. Stage 4 — Adaptation (Agent #4, second phase)

```mermaid
stateDiagram-v2
    [*] --> Gate3_Verify : ENTRY (from Stage 3)
    Gate3_Verify --> VerifyInput : merged/master.md validated

    VerifyInput --> PrepareAdapt : create ste-code/adapted/ directory

    state AdaptProcess {
        [*] --> Preserve : preserve unchanged elements
        Preserve --> Replace : replace with code-domain equivalents

        state Preserve {
            [*] --> P_Rules : all 53 rule numbers + 9-section org
            P_Rules --> P_Pipeline : 6-pass transformation pipeline
            P_Pipeline --> P_DictArch : APPROVED vs UNAPPROVED architecture
            P_DictArch --> P_TCCats : 19 Technical Code Noun categories
            P_TCCats --> P_VerbCats : 4 Technical Code Verb categories
        }

        state Replace {
            [*] --> R_Examples : STE/non-STE → code doc examples
            R_Examples --> R_Categories : aerospace categories → code-domain categories
            R_Categories --> R_Vocab : STE vocabulary → code-domain words
            R_Vocab --> R_Severity : WARNING/CAUTION → BREAKING/DEPRECATED/NOTE
            R_Severity --> R_CatMapping : apply 19-category mapping table
        }
    }

    AdaptProcess --> WriteAdapted : write adapted files to ste-code/adapted/
    WriteAdapted --> Gate4_Precheck

    state Gate4_Precheck {
        [*] --> G4_AdaptCount : ls ste-code/adapted/*.md | wc -l → ≥10
        G4_AdaptCount --> G4_RulesAdapted : all 53 rules have code-domain example pairs
        G4_RulesAdapted --> G4_SynonymTable : synonym table uses canonical forms from master.md
        G4_SynonymTable --> G4_AntiPatterns : anti-patterns are code-specific (not aerospace)
        G4_AntiPatterns --> G4_XRefs : every claim cross-references master.md entry
        G4_XRefs --> G4_NoFabrication : anti-fabrication rules 1-7 verified
        G4_NoFabrication --> G4_Pass : ALL CHECKS PASS
        G4_NoFabrication --> G4_Fail : any check fails
    }

    G4_Pass --> Stage5_Entry : PROCEED to Artifacts
    G4_Fail --> AdaptProcess : redo adaptation
```

---

## 6. Stage 5 — Artifacts (Agent #4, third phase)

```mermaid
stateDiagram-v2
    [*] --> Gate4_Verify : ENTRY (all adaptation passes)
    Gate4_Verify --> VerifyInput : adapted/ has ≥10 files

    VerifyInput --> CreateDir : mkdir -p ste-code/artifacts/

    state ArtifactGeneration {
        [*] --> A1 : ste-code-distilled-system-prompt.txt (~1,200 tokens / ~4,800 chars)
        A1 --> A2 : ste-code-self-reading-manual.txt (~7,000 tokens / ~28,000 chars)
        A2 --> A3 : ste-code-extraction-methodology.txt (~1,400 tokens / ~5,600 chars)
        A3 --> A4 : ste-code-example-turn.txt (~500 tokens / ~2,000 chars)
        A4 --> A5 : ste-code-deployment-guide.txt (~1,800 tokens / ~7,200 chars)
        A5 --> A6 : README.md (~500 tokens / ~2,000 chars)

        note right of A1 : distilled system prompt\ncondensed from full spec
        note right of A2 : self-reading manual\ncomprehensive reference
        note right of A3 : extraction methodology\nhow this was built
        note right of A4 : example turn\nannotated sample interaction
        note right of A5 : deployment guide\nhow to install and use
        note right of A6 : project README\noverview and quickstart
    }

    ArtifactGeneration --> FinalGate

    state FinalGate {
        [*] --> FG_Count : all 6 files present in ste-code/artifacts/
        FG_Count --> FG_Sizes : verify token counts within target ranges
        FG_Sizes --> FG_RulesCheck : all 53 adapted rules have code-domain pairs
        FG_RulesCheck --> FG_SynonymCheck : synonym table uses canonical forms
        FG_SynonymCheck --> FG_AntiFab : anti-fabrication rules 1-7 verified
        FG_AntiFab --> FG_XRef : every claim cross-references master.md
        FG_XRef --> FG_Pass : ALL CHECKS PASS
        FG_XRef --> FG_Fail : any check fails
    }

    FG_Pass --> PipelineComplete : 🎉 PIPELINE COMPLETE
    FG_Fail --> ArtifactGeneration : regenerate failing artifacts

    PipelineComplete --> [*]
```

---

## 7. State Transition Map — Data Flow Between Stages

```mermaid
stateDiagram-v2
    direction LR

    state extracted_dir <<directory>>
    state refined_dir <<directory>>
    state merged_dir <<directory>>
    state adapted_dir <<directory>>
    state artifacts_dir <<directory>>

    state "434 pages\nASD-STE100 Issue 9\n(January 2025)" as SpecSource

    state extracted_dir {
        w001 : w001-p1-4.md
        w002 : w002-p5-8.md
        more_w : ... 107 more files
        w109 : w109-p433-434.md
    }

    state refined_dir {
        r001 : r001-p1-4.md
        r002 : r002-p5-8.md
        more_r : ... 107 more files
        r109 : r109-p433-434.md
    }

    state merged_dir {
        master_raw : master-raw.md (concat)
        master : master.md (deduplicated, organized)
    }

    state adapted_dir {
        rules : coding-rules-*.md (≥10 files)
        dict : dictionary entries adapted
        categories : 19 categories mapped
    }

    state artifacts_dir {
        art1 : ste-code-distilled-system-prompt.txt
        art2 : ste-code-self-reading-manual.txt
        art3 : ste-code-extraction-methodology.txt
        art4 : ste-code-example-turn.txt
        art5 : ste-code-deployment-guide.txt
        art6 : README.md
    }

    SpecSource --> extracted_dir : Stage 1 — Extract\n109 workers, 4pp each
    extracted_dir --> refined_dir : Stage 2 — Refine\n109 workers, 9 rules
    refined_dir --> merged_dir : Stage 3 — Merge\nconcat + dedup + organize
    merged_dir --> adapted_dir : Stage 4 — Adapt\n19-category code mapping
    adapted_dir --> artifacts_dir : Stage 5 — Artifacts\n6 final output files

    note left of extracted_dir : 912 KB, 10,927 lines\ntotal across 109 files
    note left of refined_dir : 916 KB, 21,852 lines\ntotal across 109 files
    note left of merged_dir : 2 files:\nmaster-raw.md + master.md
    note left of adapted_dir : ≥10 files covering\nall 53 rules + 19 categories
    note left of artifacts_dir : 6 files:\n~12,400 total tokens\n~49,600 total chars
```

---

## 8. Gate Checkpoints — Full Verification Criteria

```mermaid
stateDiagram-v2
    direction TB

    state "GATE 0: Pre-Extraction" as G0 {
        [*] --> G0_1 : spec source pages exist on disk
        G0_1 --> G0_2 : ste-code/ directory structure created
        G0_2 --> G0_3 : worker-grid.md populated (109 workers, 4pp each)
        G0_3 --> G0_4 : prompt generation infrastructure ready
        G0_4 --> G0_PASS : GATE 0 ✅
    }

    state "GATE 1: Post-Extraction" as G1 {
        [*] --> G1_1 : 109 files in ste-code/extracted/
        G1_1 --> G1_2 : all files > 3KB (no truncation)
        G1_2 --> G1_3 : no zero-byte files
        G1_3 --> G1_4 : no gaps in w001-w109
        G1_4 --> G1_5 : check-rails.py passes all 4 checks
        G1_5 --> G1_6 : spot-check 3 files for real content
        G1_6 --> G1_7 : no fabrication ("TODO", "TBD", "placeholder")
        G1_7 --> G1_8 : PROGRESS.md matches disk state
        G1_8 --> G1_PASS : GATE 1 ✅
    }

    state "GATE 2: Post-Refinement" as G2 {
        [*] --> G2_1 : 109 files in ste-code/refined/
        G2_1 --> G2_2 : all files > 3KB
        G2_2 --> G2_3 : no zero-byte files
        G2_3 --> G2_4 : no gaps in r001-r109
        G2_4 --> G2_5 : all 9 refinement rules applied
        G2_5 --> G2_6 : no "..." omissions in any file
        G2_6 --> G2_7 : heading hierarchy correct (# → ## → ### → ####)
        G2_7 --> G2_8 : STE/Non-STE blockquote format correct
        G2_8 --> G2_9 : dictionary entries structured properly
        G2_9 --> G2_10 : REFINE-PROGRESS.md matches disk
        G2_10 --> G2_PASS : GATE 2 ✅
    }

    state "GATE 3: Post-Merge" as G3 {
        [*] --> G3_1 : master-raw.md exists (concatenation)
        G3_1 --> G3_2 : master.md exists (deduplicated + organized)
        G3_2 --> G3_3 : grep -c "^#### Rule" master.md = 53
        G3_3 --> G3_4 : 19 categories present and accounted for
        G3_4 --> G3_5 : ~875 APPROVED dictionary entries
        G3_5 --> G3_6 : ~1400 UNAPPROVED dictionary entries
        G3_6 --> G3_7 : section organization correct (front → Part 1 → categories → Part 2 → appendices)
        G3_7 --> G3_8 : spot-check 10 random pages against original spec
        G3_8 --> G3_PASS : GATE 3 ✅
    }

    state "GATE 4: Post-Adaptation" as G4 {
        [*] --> G4_1 : ≥10 files in ste-code/adapted/
        G4_1 --> G4_2 : all 53 rules have code-domain example pairs
        G4_2 --> G4_3 : synonym table uses canonical forms from master.md
        G4_3 --> G4_4 : anti-patterns are code-specific (not aerospace)
        G4_4 --> G4_5 : every claim cross-references master.md entry
        G4_5 --> G4_6 : anti-fabrication rules 1-7 verified
        G4_6 --> G4_7 : 19 categories (NOT 22), deepseek-v4-pro (NOT deepseek-pro)
        G4_7 --> G4_PASS : GATE 4 ✅
    }

    G0_PASS --> G1 : proceed to Extraction
    G1_PASS --> G2 : proceed to Refinement
    G2_PASS --> G3 : proceed to Merge
    G3_PASS --> G4 : proceed to Adaptation
    G4_PASS --> FINAL : proceed to Artifacts

    G0_1 --> G0_FAIL : ❌ → fix and retry
    G1_1 --> G1_FAIL : ❌ → re-launch failed workers
    G2_1 --> G2_FAIL : ❌ → re-launch + split page ranges
    G3_1 --> G3_FAIL : ❌ → redo merge from refined files
    G4_1 --> G4_FAIL : ❌ → redo adaptation
```

---

## 9. Parallelism Architecture — 3-Worker Batch Concurrency

```mermaid
stateDiagram-v2
    direction TB

    state "Batch Scheduler\n(Orchestrator Loop)" as Scheduler {
        [*] --> WritePrompts : write 3 prompt files to disk
        WritePrompts --> Launch : hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo
        Launch --> Fork

        state Fork {
            [*] --> Worker1 : WNNN (bg + notify_on_complete)
            [*] --> Worker2 : WNNN (bg + notify_on_complete)
            [*] --> Worker3 : WNNN (bg + notify_on_complete)
        }

        state "Worker Execution" as WorkerExec {
            Worker1 --> W1_Process : hermes -z reads prompt, extracts/refines pages
            Worker2 --> W2_Process : hermes -z reads prompt, extracts/refines pages
            Worker3 --> W3_Process : hermes -z reads prompt, extracts/refines pages

            W1_Process --> W1_Write : write output to disk
            W2_Process --> W2_Write : write output to disk
            W3_Process --> W3_Write : write output to disk

            W1_Write --> W1_Exit : notify_on_complete fires
            W2_Write --> W2_Exit : notify_on_complete fires
            W3_Write --> W3_Exit : notify_on_complete fires
        }

        W1_Exit --> Barrier
        W2_Exit --> Barrier
        W3_Exit --> Barrier

        Barrier --> Verify : all 3 exited
        Verify --> Commit : git add -A && git commit
        Commit --> Track : update PROGRESS.md

        state Verify {
            [*] --> SizeCheck : each file > 3KB?
            SizeCheck --> NoTrunc : no truncation?
            NoTrunc --> RulesCheck : rules applied? (refine only)
            RulesCheck --> NoOmit : no "..."? (refine only)
            NoOmit --> VerifyPass : ✅
        }

        Track --> NextBatch : 37 batches total

        state "Error Recovery" as ErrRecovery {
            SizeCheck --> SizeFail : ❌ too small
            NoTrunc --> TruncFail : ❌ truncated
            RulesCheck --> RuleFail : ❌ rules missing
            NoOmit --> OmitFail : ❌ "..." found

            SizeFail --> RecoverCheck : check disk for partial output
            TruncFail --> RecoverCheck : check disk for partial output
            RecoverCheck --> ReLaunch : re-launch specific worker
            RecoverCheck --> Split : split page range in half

            RuleFail --> ReLaunchStronger : re-launch with stronger prompt
            OmitFail --> ReLaunchStronger : mark FAILED, re-launch "never omit"
        }
    }

    note left of Fork : MAX 3 concurrent\nNever launch more\nthan 3 at once
    note left of Barrier : Wait for ALL 3\nbefore verifying
    note right of Verify : Never skip verification\nCommit only after pass
    note right of ErrRecovery : Files may exist on disk\nbefore hermes -z exits\nCheck before re-launching
```

---

## 10. Error State Machine — Failure Modes and Recovery

```mermaid
stateDiagram-v2
    direction LR

    [*] --> WorkerLaunched

    state WorkerLaunched {
        [*] --> Running : bg process active
        Running --> Timeout : > 5 minutes no output
        Running --> Crashed : process exits non-zero
        Running --> Hangs : notify_on_complete never fires
    }

    Timeout --> CheckDisk : output file on disk?
    Crashed --> CheckDisk : output file on disk?
    Hangs --> KillProcess : process kill

    state CheckDisk {
        [*] --> FileExists : file present on disk?
        FileExists --> ValidSize : size > 3KB?
        ValidSize --> NoTrunc : no truncation?
        NoTrunc --> UseExisting : ✅ use existing file
        FileExists --> FileMissing : ❌ no file
        ValidSize --> TooSmall : ❌ < 3KB
        NoTrunc --> Truncated : ❌ truncated
    }

    UseExisting --> BatchComplete : mark as done
    FileMissing --> ReLaunch : re-launch same worker
    TooSmall --> SplitPages : split page range in half
    Truncated --> SplitPages : split page range in half

    SplitPages --> SubWorker1 : launch sub-worker (first half)
    SplitPages --> SubWorker2 : launch sub-worker (second half)
    SubWorker1 --> Recombine : merge sub-outputs
    SubWorker2 --> Recombine : merge sub-outputs
    Recombine --> BatchComplete

    KillProcess --> FileMissing

    state "Fabrication Detection" as FabDetect {
        [*] --> GrepTodo : grep "TODO\|TBD\|placeholder"
        GrepTodo --> FoundSig : found → flag file
        GrepTodo --> NoSig : clean → pass
        FoundSig --> Quarantine : move to _scratch/
        Quarantine --> ReLaunchStronger : re-launch with anti-fabrication prompt
    }

    state "Content Quality" as Quality {
        [*] --> SpotCheck : random page vs original spec
        SpotCheck --> Match : content matches ✅
        SpotCheck --> Mismatch : content fabricated ❌
        Mismatch --> FlagFile : mark as FAILED
        FlagFile --> ReLaunch : re-launch worker
    }
```

---

## 11. Rails Compliance — Cross-Cutting Constraints

```mermaid
stateDiagram-v2
    direction TB

    state "R1 — Stage Isolation" as R1 {
        note: Never cross-contaminate stage directories\nExtract writes only to extracted/\nRefine writes only to refined/\netc.
    }

    state "R2 — Naming Convention" as R2 {
        note: wNNN-pPPPP-PPPP.md for extracted\nrNNN-pPPPP-PPPP.md for refined\nStrict format, no deviations
    }

    state "R3 — Completion Integrity" as R3 {
        note: Never claim completion without disk proof\nAuditor verifies all claims against filesystem
    }

    state "R4 — Content Fidelity" as R4 {
        note: Zero fabrication — every word from spec\nNo "TODO", "TBD", "placeholder", or invented content
    }

    state "R5 — Formatting Standards" as R5 {
        note: All 9 refinement rules applied\nHeadings, tables, blockquotes, spacing, lists, code blocks
    }

    state "R6 — Factual Correctness" as R6 {
        note: 19 categories (NOT 22)\n53+4 rules (NOT 65)\ndeepseek-v4-pro (NOT deepseek-pro)\n434 pages (Issue 9, Jan 2025)
    }

    state "R7 — Progress Tracking" as R7 {
        note: PROGRESS.md matches disk reality\nUpdated after EVERY batch\nAuditor re-syncs if stale
    }

    state "R8 — Error Recovery" as R8 {
        note: All fixes documented\nStale files moved to _scratch/\nNo silent overwrites without audit trail
    }

    R1 --> R2 --> R3 --> R4 --> R5 --> R6 --> R7 --> R8

    state "Auditor Verifies All Rails" as AuditCheck {
        note: Agent #3 runs disk-verified audits\nNever trusts claims alone\nCompares PROGRESS.md against filesystem\nProduces state report with PASS/FAIL per rail
    }

    AuditCheck --> R1 : verify
    AuditCheck --> R2 : verify
    AuditCheck --> R3 : verify
    AuditCheck --> R4 : verify
    AuditCheck --> R5 : verify
    AuditCheck --> R6 : verify
    AuditCheck --> R7 : verify
    AuditCheck --> R8 : verify
```

---

## 12. Complete Pipeline — All States Unified

```mermaid
stateDiagram-v2
    direction TB

    state "STE-Code Pipeline End-to-End" as Pipeline {

        state "Agent #3 — Auditor (cross-cutting)" as Auditor {
            [*] --> AuditIdle : waiting for triggers
            AuditIdle --> AuditActive : "state", "status", "report", "audit"
            AuditActive --> RunChecks : file counts, zero-byte, gaps, rails
            RunChecks --> ProduceReport : state-YYYYMMDD-HHMMSS.md
            ProduceReport --> AutoFix : move stale files, sync PROGRESS.md
            AutoFix --> FlagExchange : update exchange.md
            FlagExchange --> AuditIdle : done
        }

        state "Stage 1 — Extract (Agent #1)" as S1 {
            [*] --> S1_G0 : GATE 0
            S1_G0 --> S1_Batches : 37 batches × 3 workers
            S1_Batches --> S1_G1 : GATE 1
            S1_G1 --> S1_Done : ✅ 109/109 (912KB, 10,927 lines)
        }

        state "Stage 2 — Refine (Agent #2)" as S2 {
            [*] --> S2_G1 : GATE 1 (109 extracted)
            S2_G1 --> S2_Batches : 37 batches × 3 workers
            S2_Batches --> S2_G2 : GATE 2
            S2_G2 --> S2_Done : ✅ 109/109 (916KB, 21,852 lines)
        }

        state "Stage 3 — Merge (Agent #4)" as S3 {
            [*] --> S3_G2 : GATE 2 (109 refined)
            S3_G2 --> S3_Concat : read all 109 → master-raw.md
            S3_Concat --> S3_Dedup : deduplicate + organize
            S3_Dedup --> S3_G3 : GATE 3
            S3_G3 --> S3_Done : ✅ master.md validated
        }

        state "Stage 4 — Adapt (Agent #4)" as S4 {
            [*] --> S4_G3 : GATE 3 (master.md)
            S4_G3 --> S4_Preserve : preserve 5 immutable elements
            S4_Preserve --> S4_Replace : replace with code-domain equivalents
            S4_Replace --> S4_G4 : GATE 4 precheck
            S4_G4 --> S4_Done : ✅ ≥10 adapted files
        }

        state "Stage 5 — Artifacts (Agent #4)" as S5 {
            [*] --> S5_G4 : GATE 4 (adapted)
            S5_G4 --> S5_Gen1 : distilled-system-prompt.txt
            S5_Gen1 --> S5_Gen2 : self-reading-manual.txt
            S5_Gen2 --> S5_Gen3 : extraction-methodology.txt
            S5_Gen3 --> S5_Gen4 : example-turn.txt
            S5_Gen4 --> S5_Gen5 : deployment-guide.txt
            S5_Gen5 --> S5_Gen6 : README.md
            S5_Gen6 --> S5_Final : FINAL GATE
            S5_Final --> S5_Done : 🎉 PIPELINE COMPLETE
        }

        S1_Done --> S2 : handoff (exchange.md)
        S2_Done --> S3 : handoff (exchange.md + state report)
        S3_Done --> S4 : proceed (same agent)
        S4_Done --> S5 : proceed (same agent)

        Auditor --> S1 : audits
        Auditor --> S2 : audits
        Auditor --> S3 : audits
        Auditor --> S4 : audits
        Auditor --> S5 : audits
    }

    Pipeline --> [*] : all 5 stages complete\n6 artifacts delivered
```

---

## Pipeline Summary

| Stage | Agent | Input | Output | Workers | Files | Gate |
|-------|-------|-------|--------|---------|-------|------|
| 1 — Extract | #1 | 434 spec pages | `ste-code/extracted/` | 109 (37×3) | 109 | GATE 0 → GATE 1 |
| 2 — Refine | #2 | `extracted/` | `ste-code/refined/` | 109 (37×3) | 109 | GATE 1 → GATE 2 |
| 3 — Merge | #4 | `refined/` | `ste-code/merged/` | 1 (sequential) | 2 | GATE 2 → GATE 3 |
| 4 — Adapt | #4 | `merged/` | `ste-code/adapted/` | 1 (sequential) | ≥10 | GATE 3 → GATE 4 |
| 5 — Artifacts | #4 | `adapted/` | `ste-code/artifacts/` | 1 (sequential) | 6 | GATE 4 → FINAL |

**Agent #3 (Auditor)** operates across all stages — disk-verified, never trusts claims, enforces R1-R8 rails.

**Model:** deepseek-v4-pro exclusively. **Key facts:** 53 writing rules + 4 GR rules, 19 categories (NOT 22), 434 pages.
