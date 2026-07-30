# Per-Batch Quality Checklist

> Run after each batch of 3 workers completes.
> Check off items before launching the next batch.

## Batch __ (Workers W___ through W___)

### File Integrity
- [ ] All 3 output files exist in `ste-code/extracted/`
- [ ] File sizes: W___ (___KB), W___ (___KB), W___ (___KB)
- [ ] All sizes > 3KB (>30 lines for 4-page extraction)

### Truncation Check
- [ ] W___ last 3 lines end cleanly
- [ ] W___ last 3 lines end cleanly
- [ ] W___ last 3 lines end cleanly

Red flags (if ANY checked, re-extract):
- [ ] Last line ends mid-word
- [ ] Last line is partial table row (single `|`)
- [ ] No page footer on last page extracted

### Content Signals (check 3 random lines per file)
- [ ] "ASD-STE100 Simplified Technical English" header present
- [ ] Page footers present ("Issue 9", "2025-01-15")
- [ ] Expected content type matches page range (check section-types.md)

### Fabrication Detection
- [ ] No modern software terms in spec text ("React", "Docker", "API")
- [ ] No commentary language ("This page describes...", "The key point is...")
- [ ] Worker output reads like a spec, not a summary
- [ ] Exact text matches source when spot-checked

### State Management
- [ ] `.agents/state/PROGRESS.md` updated with [x] for this batch
- [ ] `git gcommit-hermes "Batch N: workers W___-W___ (pages ___-___)"` executed
- [ ] Feedback in `.agents/feedback/exchange.md` if issues found

## Notes
- Worker: ___
- Issues found: ___
- Actions taken: ___
