# Granular Worker Strategy (Revised)

## Problem
Original worker split (30-112 pages each) is too coarse. Workers need context headroom.

## User Directive
- **Max 3-4 pages per worker** (ideal)
- **Absolute max 10 pages per worker**
- Rationale: 1M context window should be >90% free for prompt + extraction
- Every word extracted with zero summarization pressure
- No truncation risk

## Revised Split

Total pages: 434
Pages per worker: 4 (sweet spot)
Estimated workers: 109
Batches: ~36 (3 workers per batch)
Time: ~36 × 30s = ~18 minutes (parallel batches)

### Section-by-section breakdown:

| Section | Pages | Workers (4pp) | Workers (10pp) | Notes |
|---------|-------|---------------|----------------|-------|
| Front matter + Sec 1 | 1-66 | 17 | 7 | Rules + categories = dense |
| Sec 2-5 | 67-94 | 7 | 3 | Lighter text |
| Sec 6-9 + GRs | 95-128 | 9 | 4 | GRs are short |
| Dictionary A-F | 129-240 | 28 | 12 | Most dense — dictionary entries |
| Dictionary G-P | 241-300 | 15 | 6 | Dictionary entries |
| Dictionary Q-Z | 301-360 | 15 | 6 | Dictionary entries |
| Appendices | 361-434 | 19 | 8 | Reference material |

### Worker launch template:

```bash
hermes -z "Read spec/issue-09-2025/page-XXXX.md through page-YYYY.md. Extract ALL content exactly into ste-code/workers/wNNN.md. Do not summarize. Include every word. Output ONLY markdown." -m deepseek-v4-pro --yolo
```

### Incremental save protocol:
After each batch: `git add ste-code/workers/ && git gcommit-hermes "Batch N: workers WX-WY (pages A-B)"`

### Merge protocol:
After all workers complete, concatenate by page range:
```bash
cat workers/w*.md > master-extraction.md
```
