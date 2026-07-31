# Feedback: Aphrodite CCR Tool Testing Workflow

## Date: 2026-07-31

## Problem
Other agents fail to use `aphrodite_retrieve` and CCR marker handling properly, leading to:
- Missing content when `<<<CCR:hash|type|size>>>` markers appear in tool output
- Wasted `read_file` calls re-reading files already behind CCR markers
- Failure to retrieve markers immediately when they appear

## Solution: Tested Working Process

### 1. Check engine health first
```python
aphrodite_stats()
# Must show: engine_enabled=true, proxies.token.alive=true, proxies.cache.alive=true
```

### 2. Smoke test
```python
aphrodite_test(mode="quick")
# Must return: status="ok", passed=1, total=1
```

### 3. Compress test content
```python
result = aphrodite_compress(content="Your content here", type="text")
hash = result["hash"]
```

### 4. Retrieve by hash (CRITICAL — do this immediately when you see a CCR marker)
```python
# Full content
aphrodite_retrieve(hash="the_hash_from_marker")

# Filtered (only matching lines)
aphrodite_retrieve(hash="the_hash_from_marker", query="keyword")

# Workspace file read (bypass CCR)
aphrodite_retrieve(path="README.md")  # sandbox-enforced: workspace only
```

### 5. Multi-marker handling
If a tool result contains multiple `<<<CCR:hash|type|size>>>` markers, retrieve ALL of them in the same turn before doing anything else.

## Key Rules for Agents

1. **Every `<<<CCR:hash|type|size>>>` marker IS the compressed content** — retrieve it immediately with `aphrodite_retrieve(hash=...)`
2. **Never re-read a file** when you have a live CCR marker for it — the marker IS the content
3. **Never treat markers as opaque** — they contain all the information you need
4. **If `aphrodite_retrieve` fails** (found=false), fall back to `read_file` or `terminal`
5. **Path-based reads enforce workspace containment** — paths outside the workspace return found=false

## Verified Working
This process was tested end-to-end in this session:
- `aphrodite_stats()` → both proxies alive, engine enabled
- `aphrodite_test(mode="quick")` → passed 1/1
- `aphrodite_compress(...)` → hash `f398d3a3...`, type `text`, size 172
- `aphrodite_retrieve(hash="f398d3a3...")` → full 4-line content restored
- `aphrodite_retrieve(hash="f398d3a3...", query="fox")` → only matching line returned
- `aphrodite_retrieve(path="README.md")` → workspace file read successfully
- Smoke-test hash `af488c74...` → retrieved `"fn main() { ... }"` successfully

## Related
- Full skill: `~/.hermes/skills/aphrodite-tool-testing/SKILL.md`
- Global feedback: `~/.hermes/feedback.md` (Aphrodite Tool Testing section)
- Engine config: `/Users/nikola/.hermes/aphrodite.toml` (hot-reloads on save)
- CCR database: `~/.hermes/aphrodite/ccr.db` (shared SQLite)
