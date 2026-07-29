# STE-Code Agent Handoff

Three agents complete the pipeline. Paste the relevant prompt into a new Hermes session.

## Agent #1 — Extraction Orchestrator

```
Read .hermes/agent/CONTINUE-extraction.md and follow it completely. Launch parallel hermes -z workers to extract spec pages into ste-code/extracted/. 4 pages per worker, 109 workers, 37 batches of 3. Use git gcommit-hermes after each batch.
```

## Agent #2 — Refinement Orchestrator

```
Read .hermes/agent/CONTINUE-refinement.md and follow it completely. Take the 109 raw extraction files in ste-code/extracted/ and reformat them into clean standardized markdown in ste-code/refined/. Launch 3 workers at a time. 109 total. Git after each batch.
```

## Agent #3 — Execution Auditor

```
Read .hermes/agent/CONTINUE-audit.md and follow it completely. Verify the integrity of the extraction and refinement pipeline. Cross-reference outputs, detect discrepancies, produce audit reports in ste-code/audit/. Use check-rails.py for compliance checks.
```
