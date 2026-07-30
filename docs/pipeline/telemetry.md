# Worker Telemetry

Every STE-Code worker leaves a telemetry trail at `.agents/telemetry/<worker-id>-<timestamp>.json`.

## Schema

```json
{
  "worker_id": "b1-004",
  "invocation": "hermes -z \"$(cat prompt.txt)\" -m deepseek-v4-pro --yolo",
  "prompt_file": ".agents/prompts/expansion-pass1/pass1-batch-004.txt",
  "prompt_size_bytes": 11323,
  "model": "deepseek-v4-pro",
  "reasoning_effort": "high",
  "start_time": "2026-07-30T04:16:44Z",
  "end_time": "2026-07-30T04:18:01Z",
  "duration_seconds": 77.0,
  "exit_code": 0,
  "output_file": "ste-code/adapted/expanded/pass1-batch-004.json",
  "output_exists": true,
  "output_size_bytes": 3918,
  "output_valid_json": true,
  "output_entry_count": 5,
  "self_healing": {
    "blacklist_hits": 0,
    "aerospace_terms_found": 0,
    "duplicate_entries": 0,
    "retries": 0,
    "status": "PASS"
  },
  "errors": [],
  "stderr_snippet": ""
}
```

## Fields

| Field | Description |
|-------|------------|
| `worker_id` | Batch-phase identifier (e.g., `b1-004`) |
| `duration_seconds` | Wall-clock time including model inference |
| `output_valid_json` | Whether output parses as valid JSON |
| `output_entry_count` | Number of entries/items in the output |
| `self_healing.status` | PASS, WARN (aerospace terms found), or FAIL |
| `self_healing.aerospace_terms_found` | Count of aerospace terms leaked into output (word-boundary check) |
| `errors` | Error messages from stdout/stderr |

## Querying

```bash
# Find all failed workers
python3 -c "
import json, glob
for f in sorted(glob.glob('.agents/telemetry/*.json')):
    d = json.load(open(f))
    if d['self_healing']['status'] != 'PASS' or d['exit_code'] != 0:
        print(f'{d[\"worker_id\"]}: {d[\"self_healing\"][\"status\"]} exit={d[\"exit_code\"]}')
"

# Compute total duration across all workers
python3 -c "
import json, glob
total = sum(json.load(open(f))['duration_seconds'] for f in glob.glob('.agents/telemetry/*.json'))
print(f'Total worker time: {total:.0f}s ({total/60:.1f} min)')
"
```
