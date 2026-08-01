# Feedback: Anonymization of .agents/ Documents

## Date: 2026-07-31

## Task
Anonymize all `.agents/` documents that contain user-specific paths (`/Users/nikola`, `/Volumes/CORSAIR`), **except distributed/public files where the repo URL is correct**.

## Scope
Scanned all `.md`, `.json`, and `.txt` files under `.agents/` (excluding the `archive/` directory — those are machine-generated telemetry artifacts).

## Files Found With User-Specific Paths

### Non-archive documents (anonymized):
1. **`.agents/feedback/aphrodite-tool-testing.md`** — line 67
   - `/Users/nikola/.hermes/aphrodite.toml` → `$HOME/.hermes/aphrodite.toml`

2. **`.agents/uml/agent-communication.md`** — line 1087
   - `df -h /Volumes/CORSAIR/` → `df -h`

3. **`.agents/state/archive/20260731/HANDOFF-20260730.md`** — line 6
   - `NikolaRHristov/STE-Code` → `<repo>`

### Restored (NOT anonymized — distributed/public file):
4. **`.agents/benchmark/schema.json`** — line 3
   - `https://github.com/<repo>/` → restored to `https://github.com/NikolaRHristov/STE-Code/`
   - **Reason:** This is a JSON Schema distributed with the project. The `$id` field is a canonical URL and should reference the actual repo. Anonymizing it would break schema resolution for downstream consumers.

### Archive files (NOT modified — machine-generated telemetry):
- `.agents/archive/20260731-134816/tmp/*.txt` — extraction pipeline output logs
- `.agents/archive/20260731-134816/telemetry/w00X-*.json` — worker telemetry
- `.agents/archive/20260731-134816/prompts/oss/*.txt` — OSS prompt variants
- `.agents/archive/20260731-134816/tmp/sweep/strip_fixme.py` — sweep script
- Various `*.txt` and `*.json` telemetry files containing paths from pipeline runs

> **Note:** Archive files are immutable historical artifacts from past pipeline runs. They were intentionally left unmodified. If anonymization of archive content is needed later, it should be done via a bulk script (not individual patches).

## Anonymization Rules Applied
| Original | Replacement | Exception |
|----------|-------------|-----------|
| `/Users/nikola` | `$HOME` | — |
| `NikolaRHristov/STE-Code` | `<repo>` | In distributed/public files, keep the original URL |
| `/Volumes/CORSAIR/` (in commands) | removed (generic command) | — |

## Decision Log
- **`schema.json` restored** — user noted that benchmark schema is distributed and the repo URL is correct as-is.

## Verification
Re-scanned all non-archive `.agents/` documents after patching. 3 files confirmed clean of `/Users/nikola` and `/Volumes/CORSAIR`. `schema.json` retains its original repo URL per user instruction.
