# Level 3 Session — Quick Start

## What's Ready
- 51 Level 5 summaries at `ste-code/artifacts/level5/sec*/a-sec*/summary.md`
- Assembly script at `.agents/tools/assemble-level3.py`
- Output dir at `ste-code/artifacts/level3/`

## Run

```bash
python3 .agents/tools/assemble-level3.py
```

## What It Does
Reads all 51 Level 5 summaries, groups by section, produces 9 section-level grammar summaries (~20K tokens total). One example pair per section.

## Level Assembly Chain
```
Level 5 (100K) → assemble-level4.py → Level 4 (50K)
Level 5 (100K) → assemble-level3.py → Level 3 (20K)
Level 3 (20K)  → compress manually   → Level 2 (5K)
Level 2 (5K)   → compress manually   → Level 1 (1.2K)
```
