---
name: release-claim-verification
description: Verify release-note claims at a git tag, not HEAD.
---

# Release claim verification

Verifying the claims a **published** document makes about itself — release
notes, READMEs, quality boasts, benchmark headlines — against the tree at the
revision those claims describe.

**Distinct from two neighbours.** `iterative-diff-research` verifies numbers
derived from a *diff*. Release drift tooling (`facts.py`, `scan.py`) verifies
the *working tree* before publishing. This skill verifies a *past* document
against a *past* rev. Using either neighbour for that job manufactures
contradictions that do not exist.

**Draft only.** Produce a findings log. Never commit, tag, or push during an
audit.

## When to use this

- "Re-research `<base>..<tip>` and verify the vN.M.O note's claims"
- Hunting count contradictions across releases or between sibling docs
- Deciding whether a number in a note is wrong, or the repo is inconsistent
- Before re-publishing or correcting an existing release body

## Golden rule

> Measure at the rev the document describes. Never at HEAD. Never from another
> document.

Counts move between releases. The worked case (STE-Code, `bb1b29a..0cf59e4`):

| Tag | Writing rules | GR | Total units |
|---|---|---|---|
| `STANDARD-1.0.0` | 51 | 4 | 55 |
| `v1.0.0` | **51** | 4 | **55** |
| `v1.1.0` | **54** | 4 | 58 |
| `HEAD` | **54** | 4 | 58 |

Three rules (`a-sec2-rule2.3`, `a-sec6-rule6.6`, `a-sec8-rule8.7`) landed
*after* v1.0.0. `.agents/AGENTS.md`'s "54 rules … 60 files" describes v1.1.0+,
not v1.0.0 (51 + 4 + 2 = 57 files). Judging the v1.0.0 note against AGENTS.md
would "find" a rule-count error that was never there.

## Procedure

1. **Pin the range.** `git log --oneline -1 <base>`, `-1 <tip>`,
   `git tag --list`. Record which tags fall inside the range.
2. **Read the document under audit.** List every falsifiable claim — counts,
   percentages, file paths, feature assertions.
3. **Measure each at the rev** with the cookbook below. One command per claim.
4. **Log incrementally.** Write the file after the first block of claims, not
   at the end (see Report shape).
5. **Classify** with the four-verdict taxonomy. Never collapse to true/false.
6. **Separate fault** — claims the note got wrong vs. repo contradictions it
   faithfully inherited.
7. **Close** with a copy-pasteable "safe numbers" line for the note author.

## Cookbook — inspect a rev without checking it out

Never `git checkout` to audit; other sessions write in this tree. All read-only:

```bash
REV=v1.0.0   # or the SHA

git ls-tree --name-only $REV path/dir/          # list at rev
git ls-tree -r --name-only $REV path/dir/       # recursive

git ls-tree --name-only $REV ste-code/adapted/ | grep -c 'rule'
git show $REV:path/to/file.md | grep -c '^## Category'

git show $REV:path/to/file.md | sed -n '20,60p'          # read at rev
git cat-file -s $(git rev-parse $REV:path/file.txt)      # byte size
git cat-file -e $REV:path/file.md 2>/dev/null \
  && echo EXISTS || echo MISSING                          # dangling refs
git grep -n 'FIXME' $REV -- 'ste-code/'                  # rev BEFORE --

# CRLF audit at a rev
for f in $(git ls-tree -r --name-only $REV ste-code/ | grep -E '\.(md|txt|json|py)$'); do
  git show $REV:"$f" | grep -qU $'\r' && echo "CRLF: $f"
done

# What changed between two tags
diff <(git ls-tree --name-only v1.0.0 ste-code/adapted/) \
     <(git ls-tree --name-only HEAD    ste-code/adapted/)
```

## Status taxonomy

Four verdicts — true/false loses the important middle.

| Status | Meaning |
|---|---|
| **VERIFIED** | Reproduced from disk at the rev. Cite the command. |
| **DISPUTED** | Measured, disagrees. Give the right number **and** where the wrong one came from. |
| **PARTIAL** | Defensible but misleading as written; needs a qualifier. |
| **UNVERIFIABLE** | No artifact at the rev settles it. Not the same as false. |

Tracing *where a wrong number came from* is not optional — it is usually what
tells the author how to fix it, and it often exonerates the note.

## Pitfalls

Each of these produced a wrong first impression before being measured.

1. **A headline that is a sum is not a contradiction.** "55 adapted rules" and
   "51 writing rules + 4 grammar recommendations" are one claim at two
   granularities. Check `a + b == headline` before reporting a conflict.

2. **Front-matter may describe the SOURCE, not the artifact.** A dictionary
   header reading `~875 approved | ~1274 unapproved` describes the *input*
   spec (ASD-STE100 pages 149–434). Summing them produced a note's "2,149
   dictionary entries"; the file held **560** adapted entries
   (`grep -cE '^## [A-Z].*\([a-z]+\)'`). Overstated ~3.8×. A `~` on either side
   of a sum is a red flag.

3. **`grep -c` alone manufactures false contradictions.** "0 FIXME markers"
   looked refuted by 6 hits; `grep -n` showed all six legitimate — the quality
   claim itself, `"FIXME"` in vocabulary lists, and a rule *teaching* `FIXME:`
   as an approved noun. VERIFIED in substance. Always read matched lines before
   disputing a zero-claim.

4. **Asymmetric evidence between a claim and its comparison partner.** A
   control result (11.9%) had a committed `aggregate-results.json`; the
   headline (96.6%) had 59 prompt + 59 output files and **no scored artifact**
   — `rescore.py` was never run and committed. The run is real; the score is
   prose-only → UNVERIFIABLE. When a note says "X% vs Y%", check **both** sides
   have artifacts.

5. **Dangling references hide behind confident prose.** `git cat-file -e`
   caught a referenced-but-absent `artifacts/sweep-report.md`, and a
   `linguistics/SPECIFICATION.md` absent at the tag **and at HEAD** that 4 of
   12 advertised FLAVOR layers anchor their links to. Check HEAD too: "missing
   then, still missing now" is a far stronger finding.

6. **Specified ≠ implemented.** 12 checking layers specified in `FLAVOR.md`, 5
   implemented in `ste_code_lint.py`. Prefer "12 specified, 5 enforced".

7. **Counting containers vs counting artifacts.** "5 level system prompts" —
   5 *levels* existed but only 4 `system-prompt.txt` files (level5 was 51
   per-rule summary dirs, level0 a bare `.gitkeep`). The repo's own README said
   "5 levels, 4 system prompts". The stated "1.2K–45K" range also spanned only
   L1–L4 (L5 ≈ 100K) — two halves of one claim disagreeing.

8. **Off-by-one across sibling docs.** "18 workflows" vs 17 defined — traced to
   `ROADMAP.md` Phase 3 citing "Workflows 6–10, 12–13, 15–18", a Workflow 18
   that `WORKFLOWS.md` never defines. When a count is off by one, grep siblings
   for the phantom item.

9. **Labels get redefined between releases — never cross-quote.** "Level 1" was
   ~1.2K tokens / 4,473 B at v1.0.0 and 58 KB / ~14.5K at HEAD, which also adds
   levels −2/−1/0. Same label, different artifact.

10. **"Unchanged for consumers" needs a floor.** "54 rules, unchanged" was true
    *since v1.1.0* and false back to v1.0.0 (51). Stability claims without a
    starting release are cross-release errors.

11. **Stale "immutable facts" in older audit guidance.** Pipeline-era skills in
    this repo still assert 19 categories / 53 rules and even list an auto-fix
    `22 categories → 19`. Measured at v1.0.0 and at HEAD it is **22**. Measure;
    do not apply that auto-fix.

12. **Initial-import ranges inflate the headline diff.** `+113,800/−34,521`
    over 1,850 files is creation volume, not churn, when the range starts at
    the repo's first commit. Say so, or the stat reads as massive rewriting.

## Report shape

Write incrementally to `.agents/tmp/research-findings-<version>.md`. Land range
identity, headline stats, and the first verified claims **before** finishing
the sweep, so a long audit survives a timeout.

1. Range identity table (first commit, tip, tags in play)
2. Headline stats, with the initial-import caveat where it applies
3. Verified-counts table: metric | value | **the exact command**
4. Verified claims, numbered, each citing evidence
5. Disputed/corrected, each with the right value **and** the wrong one's origin
6. Additional findings (repo-internal contradictions, not the note's fault)
7. Open items, ending with a copy-pasteable "safe numbers for the notes" line

Close the reply with a one-line receipt: path, line count, and the
verified/disputed/partial tally.

## Appendix — v1.0.0 result (`bb1b29a..0cf59e4`)

**12 verified · 3 disputed · 3 partial · 6 inherited repo contradictions.**

Measured at the tag: 51 rules + 4 GR = 55 units; 22 categories; 560 dictionary
entries (452 approved / 108 UNNAPROVED); 4 assembled prompts (4,473 / 17,884 /
31,160 / 126,528 B) + level5 summaries + standalone `level5-max.txt` 228,903 B;
12 FLAVOR layers; 17 workflows; 59 tests / 14 category files with 59 real
prompt+output pairs; 0 CRLF; 65 files × 2 sweeps (5 batches × 13). Range diff:
1,850 files, +113,800 / −34,521, 159 commits (148 non-merge + 11 merge).

Disputed: 2,149 dictionary entries → 560; 18 workflows → 17; 5 system prompts
→ 4. Partial/unverifiable: 96.6% pass rate (prose-only); "supports
Claude/Codex" (commented-out stubs, only `hermes` configured); "6-phase
roadmap" (7 phases, numbered 0–6).

Inherited contradictions: `artifacts/README.md` says 19 categories (actual 22);
`ste-code/README.md` says "53 rules" while its own Stage 4 box says "51 rules +
4 GR"; missing `sweep-report.md`; missing `SPECIFICATION.md`; linter covers 5
of 12 layers.

Safe numbers for those notes: 55 rule units (51 + 4) · 22 categories · 560
dictionary entries · 4 assembled prompts + level-5 spec · 12 specified layers
(5 enforced) · 17 workflows · 59 tests / 14 categories · 65 files in 2 passes ·
0 FIXME · 0 CRLF · control 11.9% verified.
