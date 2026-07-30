# Workers

All STE-Code pipeline stages use the same worker pattern.

## Launch Command

```bash
python3 .agents/tools/telemetry-worker.py <worker-id> <prompt-file> --output <output-file>
```

## Pattern

```
WRITE prompt to file
  → LAUNCH: telemetry-worker.py with bg + notify_on_complete
  → WAIT for all 3 in batch to exit
  → VERIFY: telemetry shows PASS, output exists, valid content
  → COMMIT: git gcommit-hermes
  → NEXT batch
```

## Self-Healing

Before writing output, every worker:
1. Checks if output already exists with valid content → SKIP
2. Verifies input dependencies exist on disk → RECOVERY-NEEDED if missing
3. Validates output against schema/format rules → retry once on failure
4. Checks for duplication against blacklist → generate alternative
5. Reports: `[PASS|SKIP|RETRY|RECOVERY]` + metrics

## Worker Template

Workers are launched via generated prompt files. Template:
```
SYSTEM PROMPT (STE-Code rules)
AGENT PROTOCOL (task-specific instructions)
TASK (what to produce)
INPUT (files to read)
DEDUP BLACKLIST (what not to repeat)
OUTPUT FORMAT (JSON schema or markdown structure)
RECOVERY INSTRUCTIONS (what to do on failure)
```

## File Naming

- Extraction: `ste-code/extracted/wNNN-pPPPP-PPPP.md`
- Refinement: `ste-code/refined/rNNN-pPPPP-PPPP.md`
- Expansion: `ste-code/adapted/expanded/passN-batch-NNN.json`
- Telemetry: `.agents/telemetry/<worker-id>-<timestamp>.json`
- Recovery: `RECOVERY-NEEDED/<worker-id>.md`
