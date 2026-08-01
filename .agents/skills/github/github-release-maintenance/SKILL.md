---
name: github-release-maintenance
description: "Use when releasing STE-Code or auditing version/badge/count drift. One command syncs badges, docs, changelog, labels, tags, and the GitHub release."
version: 1.0.0
author: Nikola Hristov
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Release, GitHub, Versioning, Changelog, Badges, CI, Maintenance]
    related_skills: [github-pr-workflow, github-repo-management, github-auth]
---

# STE-Code Release Maintenance

One skill that owns everything a release touches: measured project facts,
badges, version stamps, count claims in prose, the changelog, git tags on all
three tracks, the GitHub release, and repository labels and topics.

**Not shippable.** This is repository maintenance tooling — it lives in
`.agents/`, never inside `ste-code/`.

## When to use this

- Cutting a release (`v1.1.0`, `STANDARD-1.1.0`, `FLAVOR-1.1.0`)
- A number changed on disk (rules, categories, tiers, locales, tests) and the
  documentation must catch up
- CI reported fact drift
- Auditing what STE-Code claims about itself before publishing

## The single command

```bash
# See everything that would change. Nothing is written.
python3 .agents/tools/release/release.py --bump minor --dry-run

# Apply it.
python3 .agents/tools/release/release.py --bump minor --execute
```

`--bump {major,minor,patch}` derives the version from the newest `vX.Y.Z` tag;
`--version 1.1.0` sets it explicitly. **Default is dry run** — `--execute` is
always required to write.

## Tooling map

| Tool | Purpose |
|------|---------|
| `.agents/tools/release/facts.py` | Measures the project from disk. The only authority for every number. |
| `.agents/tools/release/registry.json` | Every claim site: badges, version stamps, count patterns, labels, topics. |
| `.agents/tools/release/scan.py` | Finds claims that disagree with `facts.py`. Exit 1 on drift. |
| `.agents/tools/release/sync.py` | Rewrites drifted claims in place. |
| `.agents/tools/release/changelog.py` | Rebuilds `CHANGELOG.md` from git history. |
| `.agents/tools/release/release.py` | Orchestrates all ten steps. |
| `.agents/tools/release/test_release.py` | 55 self-tests. No network, no git writes. |
| `.agents/tools/release/prompts/audit.md` | LLM prompts for the judgement calls the tools refuse to make. |
| `.github/workflows/release.yml` | CI drift gate + manual release dispatch. |

## Verify the tooling itself

```bash
make lint     # compile + line length, includes .agents/tools/release/
make test     # benchmark selftest + release selftest (55 checks)
make drift    # the claim scan on its own
make check    # lint + test + audit
```

`test_release.py` exercises the **write** paths (`apply_line_fix`,
`apply_stamp_fix`) against throwaway files in `.agents/tmp/release-selftest/`,
never against real claim sites, and tears the sandbox down afterwards.

## Step 1 — Measure

```bash
python3 .agents/tools/release/facts.py
```

Facts are measured, never typed: rules are counted from
`ste-code/final/rules/a-sec*-rule*.md`, categories from `## Category N`
headings, tier sizes are delegated to `measure_artifacts.py` (real `o200k_base`
tokens), and versions come from git tags.

## Step 2 — Scan for drift

```bash
python3 .agents/tools/release/scan.py          # curated sync set (gating)
python3 .agents/tools/release/scan.py --wide   # every tracked doc (advisory)
python3 .agents/tools/release/scan.py --json
```

Exit code 0 = clean, 1 = drift. CI gates on the default (non-`--wide`) run.

## Step 3 — Sync

```bash
python3 .agents/tools/release/sync.py --dry-run
python3 .agents/tools/release/sync.py
python3 .agents/tools/release/sync.py --pick categories-count=22
```

Unambiguous claims are rewritten automatically. Ambiguous ones are **never
guessed** — see "Ambiguous counts" below.

## Step 4 — Changelog

```bash
python3 .agents/tools/release/changelog.py --stdout
python3 .agents/tools/release/changelog.py --next 1.1.0
python3 .agents/tools/release/changelog.py --notes 1.1.0   # release body
```

Rebuilt from git every time, so it covers **past and present**: an
`Unreleased` section plus one section per existing tag. Conventional Commit
types map to Keep-a-Changelog headings; `poll-commit`, `Phase X:`, `wip`, and
merges are filtered as pipeline noise.

## Step 5 — Tag, publish, label

`release.py` tags all three tracks (`v`, `STANDARD-`, `FLAVOR-`), pushes,
creates the GitHub release with generated notes, then reconciles the labels and
topics in `registry.json`. Narrow with `--tracks core`, `--no-push`,
`--no-publish`.

## Ambiguous counts — the important pitfall

"Categories" means two different things in this repo: **22** technical-noun
categories in the standard, and **14** benchmark test categories. "Rules" is
**54** adapted rules, but refinement docs legitimately describe their own "9
rules". So each count claim in `registry.json` carries a **set** of acceptable
facts, and a line is only flagged when it matches none of them.

Three ways to resolve a flag:

1. It is genuinely stale → let `sync.py` fix it (or `--pick claim=value`).
2. It is a different quantity that happens to collide → append
   `<!-- release-scan:ignore -->` to that line.
3. The scanner is systematically wrong → tighten the pattern in
   `registry.json`.

Never widen a pattern just to make the scan pass.

## When to ask an LLM

The tools own numbers; they deliberately refuse judgement. `prompts/audit.md`
holds three ready prompts for the cases that need meaning rather than digits:

| Prompt | Use it when |
|--------|-------------|
| Resolve an ambiguous count | `sync.py` reports "ambiguous — use `--pick`" |
| Review generated release notes | Before publishing, to catch vague or noisy entries |
| Post-release documentation sweep | Stale *prose* a regex cannot see (wrong stage names, dead paths) |

Each prompt is fed the measured facts and forced to pick among tool-supplied
candidates, so the model classifies and never invents a number. A verdict of
`STALE` becomes a `--pick`; `OTHER` or `QUOTE` becomes an
`<!-- release-scan:ignore -->` comment.

## Known live drift (2026-08-01)

Pre-existing errors this tooling surfaced, kept here so a future run recognises
them rather than rediscovering them:

- `CITATION.cff:6` — "53 rules, 19 categories" (both from an earlier count;
  now 54 and 22)
- `CONTRIBUTING.md:37` — "53 writing rules"; `:245` — "51 adapted rules"
- `.agents/AGENTS.md:184` — "53 rules → code domain, 19 categories"
- `.agents/AGENTS.md:72,192` — "9 locales" (there are 10)

`--wide` also flags the historical audit narratives in `.agents/agent/` that
*quote* wrong numbers on purpose ("Error: claimed 22 categories"). Those are
records of past mistakes — leave them.

## Pitfalls

- **`tiktoken` is required** for tier measurement. Without it, tier facts come
  back empty and tier claims are silently skipped. `pip install tiktoken`.
- **Two page counts are both correct.** The source PDF has 434 printed pages;
  the split produces 426 page files. `facts.py` exposes `spec_pdf_pages` and
  `spec_pages` separately — do not collapse them.
- **Never scan pipeline output.** `ste-code/artifacts/`, `adapted/`, `final/`,
  and the locale directories are full of numbers that belong to the standard's
  own examples ("version 3.0 of the library"). They are excluded in
  `registry.json` — keep it that way.
- **The tree must be clean** before `--execute`, or preflight refuses. This is
  deliberate: the release commits with `git add -A`.
- **Benchmark output is ignored by design.** The benchmark badge only syncs
  when a committed summary exists; runs under `.agents/benchmark/tests/` are
  gitignored, so a fresh run does not move the badge on its own.
- **`gh` must be authenticated** for publishing and labels. Without it those
  steps are skipped, not failed.
- **Multi-session safety.** A release does `git add -A`. Do not run it while
  another Hermes session is mid-write in `ste-code/refined/` or
  `ste-code/grouped/`.

## Verification after a release

```bash
python3 .agents/tools/release/scan.py            # must exit 0
git tag --list | tail -5                         # three new tags
gh release view v1.1.0                           # notes published
head -20 CHANGELOG.md                            # new section on top
```
