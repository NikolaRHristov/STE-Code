# STE-Code final/ Progress Tracker

> **⚠️ Stale-flag source of truth.** A row marked `stale` means
> `ste-code/final/rules/<file>` is byte-identical to `ste-code/adapted/<file>`
> — i.e. it was copied, NOT LLM-synthesized. Those files MUST be re-synthesized
> by an agent session (the agent reads adapted/ + references and writes the
> enriched file itself). A row marked `enriched` is a real LLM synthesis.
>
> Regenerate this table any time with:
> `python3 .agents/tools/finalize/finalize_batch.py --regen-progress`
> (written to .agents/state/finalize-progress.md — ste-code/ is shippable).
> The execution auditor cross-references these claims against disk evidence.

## Status legend
- `enriched` — LLM-synthesized final rule (differs from adapted source)
- `stale`    — copied from adapted/ (NOT synthesized; must be re-run)

## Rule status

| # | File | Status | Note |
|---|------|--------|------|
| 1.1.1 | a-sec1-rule1.1.md | enriched | LLM final |
| 1.1.10 | a-sec1-rule1.10.md | enriched | LLM final |
| 1.1.11 | a-sec1-rule1.11.md | enriched | LLM final |
| 1.1.12 | a-sec1-rule1.12.md | enriched | LLM final |
| 1.1.13 | a-sec1-rule1.13.md | enriched | LLM final |
| 1.1.14 | a-sec1-rule1.14.md | enriched | LLM final |
| 1.1.2 | a-sec1-rule1.2.md | enriched | LLM final |
| 1.1.3 | a-sec1-rule1.3.md | enriched | LLM final |
| 1.1.4 | a-sec1-rule1.4.md | enriched | LLM final |
| 1.1.5 | a-sec1-rule1.5.md | enriched | LLM final |
| 1.1.6 | a-sec1-rule1.6.md | enriched | LLM final |
| 1.1.7 | a-sec1-rule1.7.md | stale | copied; re-synthesize |
| 1.1.8 | a-sec1-rule1.8.md | enriched | LLM final |
| 1.1.9 | a-sec1-rule1.9.md | enriched | LLM final |
| 2.2.1 | a-sec2-rule2.1.md | enriched | LLM final |
| 2.2.2 | a-sec2-rule2.2.md | enriched | LLM final |
| 2.2.3 | a-sec2-rule2.3.md | enriched | LLM final |
| 3.3.1 | a-sec3-rule3.1.md | stale | copied; re-synthesize |
| 3.3.2 | a-sec3-rule3.2.md | stale | copied; re-synthesize |
| 3.3.3 | a-sec3-rule3.3.md | stale | copied; re-synthesize |
| 3.3.4 | a-sec3-rule3.4.md | stale | copied; re-synthesize |
| 3.3.5 | a-sec3-rule3.5.md | stale | copied; re-synthesize |
| 3.3.6 | a-sec3-rule3.6.md | stale | copied; re-synthesize |
| 3.3.7 | a-sec3-rule3.7.md | stale | copied; re-synthesize |
| 4.4.1 | a-sec4-rule4.1.md | stale | copied; re-synthesize |
| 4.4.2 | a-sec4-rule4.2.md | stale | copied; re-synthesize |
| 4.4.3 | a-sec4-rule4.3.md | stale | copied; re-synthesize |
| 4.4.4 | a-sec4-rule4.4.md | stale | copied; re-synthesize |
| 4.4.5 | a-sec4-rule4.5.md | stale | copied; re-synthesize |
| 5.5.1 | a-sec5-rule5.1.md | stale | copied; re-synthesize |
| 5.5.2 | a-sec5-rule5.2.md | stale | copied; re-synthesize |
| 5.5.3 | a-sec5-rule5.3.md | stale | copied; re-synthesize |
| 5.5.4 | a-sec5-rule5.4.md | stale | copied; re-synthesize |
| 5.5.5 | a-sec5-rule5.5.md | stale | copied; re-synthesize |
| 6.6.1 | a-sec6-rule6.1.md | stale | copied; re-synthesize |
| 6.6.2 | a-sec6-rule6.2.md | stale | copied; re-synthesize |
| 6.6.3 | a-sec6-rule6.3.md | stale | copied; re-synthesize |
| 6.6.4 | a-sec6-rule6.4.md | stale | copied; re-synthesize |
| 6.6.5 | a-sec6-rule6.5.md | stale | copied; re-synthesize |
| 6.6.6 | a-sec6-rule6.6.md | stale | copied; re-synthesize |
| 7.7.1 | a-sec7-rule7.1.md | stale | copied; re-synthesize |
| 7.7.2 | a-sec7-rule7.2.md | stale | copied; re-synthesize |
| 7.7.3 | a-sec7-rule7.3.md | stale | copied; re-synthesize |
| 8.8.1 | a-sec8-rule8.1.md | stale | copied; re-synthesize |
| 8.8.2 | a-sec8-rule8.2.md | stale | copied; re-synthesize |
| 8.8.3 | a-sec8-rule8.3.md | stale | copied; re-synthesize |
| 8.8.4 | a-sec8-rule8.4.md | stale | copied; re-synthesize |
| 8.8.5 | a-sec8-rule8.5.md | stale | copied; re-synthesize |
| 8.8.6 | a-sec8-rule8.6.md | stale | copied; re-synthesize |
| 8.8.7 | a-sec8-rule8.7.md | stale | copied; re-synthesize |
| 9.9.1 | a-sec9-rule9.1.md | stale | copied; re-synthesize |
| 9.9.2 | a-sec9-rule9.2.md | stale | copied; re-synthesize |
| 9.9.3 | a-sec9-rule9.3.md | stale | copied; re-synthesize |
| 9.9.4 | a-sec9-rule9.4.md | stale | copied; re-synthesize |

## Summary
- enriched: 16 / 54
- stale (must re-synthesize): 38 / 54
