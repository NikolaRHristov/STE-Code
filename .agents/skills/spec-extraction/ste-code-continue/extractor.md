# Agent #1 — Extraction Orchestrator

You are the STE-Code Extraction Orchestrator. Your job: extract the 434-page
ASD-STE100 Issue 9 spec using 109 parallel `hermes -z` workers, each processing
exactly 4 pages. Launch in 37 batches of 3.

## Verify Environment

```bash
ls spec/issue-09-2025/ | head -5    # Must show page files
ls spec/issue-09-2025/ | wc -l      # Must be 434+
mkdir -p ste-code/extracted .agents/prompts/refine
```

## Worker Command Template

```bash
hermes -z "Read spec/issue-09-2025/page-<<START>>.md through page-<<END>>.md.
Extract ALL content exactly into ste-code/extracted/w<<NNN>>-p<<START>>-<<END>>.md.
Do not summarize. Include every word, every table, every example.
Output ONLY the markdown file." -m deepseek-v4-pro --yolo
```

## Launch Rules

- Always use `hermes -z "$(cat .agents/prompts/refine/wNNN-prompt.txt)" -m deepseek-v4-pro --yolo`
- Always launch exactly 3 workers per batch (never more)
- Always verify output after each batch before launching next
- Never use inline extraction — it defeats parallelization
- Never exceed 4 pages per worker (prevents truncation)
- Always save state: `git gcommit-hermes "Batch N complete"` after each batch
- Save generated prompts to `.agents/prompts/refine/wNNN-prompt.txt`

## Worker Grid (37 batches × 3 workers, 109 total)

```
Batch 01: W001(1-4)   W002(5-8)   W003(9-12)
Batch 02: W004(13-16) W005(17-20) W006(21-24)
Batch 03: W007(25-28) W008(29-32) W009(33-36)
Batch 04: W010(37-40) W011(41-44) W012(45-48)
Batch 05: W013(49-52) W014(53-56) W015(57-60)
Batch 06: W016(61-64) W017(65-68) W018(69-72)
Batch 07: W019(73-76) W020(77-80) W021(81-84)
Batch 08: W022(85-88) W023(89-92) W024(93-96)
Batch 09: W025(97-100) W026(101-104) W027(105-108)
Batch 10: W028(109-112) W029(113-116) W030(117-120)
Batch 11: W031(121-124) W032(125-128) W033(129-132)
Batch 12: W034(133-136) W035(137-140) W036(141-144)
Batch 13: W037(145-148) W038(149-152) W039(153-156)
Batch 14: W040(157-160) W041(161-164) W042(165-168)
Batch 15: W043(169-172) W044(173-176) W045(177-180)
Batch 16: W046(181-184) W047(185-188) W048(189-192)
Batch 17: W049(193-196) W050(197-200) W051(201-204)
Batch 18: W052(205-208) W053(209-212) W054(213-216)
Batch 19: W055(217-220) W056(221-224) W057(225-228)
Batch 20: W058(229-232) W059(233-236) W060(237-240)
Batch 21: W061(241-244) W062(245-248) W063(249-252)
Batch 22: W064(253-256) W065(257-260) W066(261-264)
Batch 23: W067(265-268) W068(269-272) W069(273-276)
Batch 24: W070(277-280) W071(281-284) W072(285-288)
Batch 25: W073(289-292) W074(293-296) W075(297-300)
Batch 26: W076(301-304) W077(305-308) W078(309-312)
Batch 27: W079(313-316) W080(317-320) W081(321-324)
Batch 28: W082(325-328) W083(329-332) W084(333-336)
Batch 29: W085(337-340) W086(341-344) W087(345-348)
Batch 30: W088(349-352) W089(353-356) W090(357-360)
Batch 31: W091(361-364) W092(365-368) W093(369-372)
Batch 32: W094(373-376) W095(377-380) W096(381-384)
Batch 33: W097(385-388) W098(389-392) W099(393-396)
Batch 34: W100(397-400) W101(401-404) W102(405-408)
Batch 35: W103(409-412) W104(413-416) W105(417-420)
Batch 36: W106(421-424) W107(425-428) W108(429-432)
Batch 37: W109(433-434) — 2 pages only, last batch
```

Full grid also at: `.agents/skills/spec-extraction/references/worker-grid.md`

## Quality Checks (Per Batch)

After each batch of 3 workers completes:

1. **File check**: All 3 output files exist in `ste-code/extracted/`
2. **Size check**: Each file > 3KB (>30 lines)
3. **Truncation check**: Last 3 lines end cleanly (period, footer, or table row)
4. **Content signal**: Expected keywords present (`grep "ASD-STE100" ste-code/extracted/wNNN-p*.md`)
5. **Fabrication check**: No commentary ("This page describes..."), no modern terms
6. **Tracking check**: PROGRESS.md updated to reflect this batch ✅

If any check fails, re-extract with the worker's page range split in half.

## 🔴 MANDATORY: Update PROGRESS.md After Every Batch

The execution auditor cross-references PROGRESS.md against disk. A stale PROGRESS.md
is a 🔴 CRITICAL discrepancy. After each batch:

1. Flip the batch's `[ ]` to `✅` in `.agents/state/PROGRESS.md`
2. Update the progress counter
3. `git add` and `git commit`

## Immutable Facts

- 19 technical noun categories (NOT 22)
- deepseek-v4-pro model (NOT deepseek-pro or deepseek-v4-flash)
- Output: `ste-code/extracted/wNNN-pPPPP-PPPP.md`
- 109 workers × 4 pages = 434 pages total
- Follow `.agents/skills/spec-extraction/references/rails.md` — all 8 guardrails apply

## Start Now

1. Verify spec pages exist: `ls spec/issue-09-2025/ | head -5`
2. Generate prompts for Batch 1 (W001, W002, W003), save to `.agents/prompts/refine/`
3. Launch 3 workers via `hermes -z` with `--yolo`
4. Wait for completion, verify output, update PROGRESS.md
5. Continue through all 37 batches
