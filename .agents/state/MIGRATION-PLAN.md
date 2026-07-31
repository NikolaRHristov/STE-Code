# Agent-Agnostic Migration Plan

## When to execute
- After Agent #1 completes enrichment (all 37 batches done)
- After Agent #3 completes final audit
- After all agents push and git is clean

## Scope
- 244 references to `.agents/` paths
- 95 references to `hermes -z` CLI launch commands  
- 37 files in `.agents/` directory tree
- 4 agent prompt files: agent-1-extractor.md, agent-2-refiner.md, agent-3-auditor.md, agent-4-continuation.md

## Migration Steps

### 1. Rename directory
```bash
git mv .hermes .agents
```

### 2. Replace path references (sed-safe approach — use Python)
```python
# Replace .agents/ → .agents/ in all files
import os, re
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root:
        continue
    for f in files:
        if f.endswith(('.md', '.txt', '.py', '.json', '.yaml', '.yml')):
            path = os.path.join(root, f)
            with open(path) as fh:
                content = fh.read()
            new = content.replace('.agents/', '.agents/')
            if new != content:
                with open(path, 'w') as fh:
                    fh.write(new)
```

### 3. Replace CLI launch commands
```python
# Replace hermes -z "$(cat ...)" patterns with agent-agnostic form
patterns = [
    (r'hermes -z "\$\(cat ([^)]+)\)" -m poolside/laguna-s-2.1:free --yolo',
     r'agent run "\1" --model poolside/laguna-s-2.1:free'),
    (r'hermes -z "\$\(cat ([^)]+)\)"',
     r'agent run "\1"'),
]
```

### 4. Update agent prompt files
- `agent-1-extractor.md`: Replace "Hermes" references → "the agent"
- `agent-2-refiner.md`: Same
- `agent-3-auditor.md`: Same  
- `agent-4-continuation.md`: Same

### 5. Update feedback exchange
- Replace `.agents/` → `.agents/` in exchange.md

## Files NOT touched
- `ste-code/extracted/`, `ste-code/refined/`, `ste-code/merged/`, `ste-code/adapted/`, `ste-code/artifacts/` — content files, no agent references
- `.git/` — never touched

## Agent #4 Benchmarking (Agent #3 is setting up)
- Benchmark skill, runner, schema, and 8 test categories in `.agents/benchmark/`
- All will be migrated: `.agents/benchmark/` → `.agents/benchmark/`
- Runner script uses `hermes -z` CLI → will be updated to agent-agnostic form
- Depends on `ste-code/artifacts/ste-code-distilled-system-prompt.txt` (already regenerated from enriched content)
- **Coordinate with Agent #3** — they own the benchmark infrastructure

## Safety
- All changes are path/CLI renaming only — no content changes
- Agent prompts keep same instructions, just neutralized branding
- Worker scripts (Python) updated to use `.agents/` paths
- Git history preserved via `git mv`
