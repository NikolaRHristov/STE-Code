---
name: git-range-forensics
description: Ground-truth a commit range before trusting its numbers.
---

# Git range forensics

Establishing **what a commit range actually contains** — before any claim,
changelog line, or headline stat derived from it is trusted.

This is the measurement substrate underneath three neighbours:
`release-claim-verification` (audits a published note against a rev),
`iterative-diff-research` (turns a big diff into an incremental report), and
`github-release-maintenance` (publishes the numbers). All three inherit errors
made here. Get the range identity wrong and every downstream figure is wrong in
a way that looks authoritative.

## When to use this

- Inheriting stats from an earlier pass ("591 commits, 2,622 files,
  +322k/−161k")
- Re-researching `<base>..<tip>` for any purpose
- A cited commit hash needs to be confirmed as part of _this_ release
- A changelog line's scope or attribution looks bigger than the commit
- Reconciling two passes that measured the same range and disagree

## Golden rule

> A number is a range number only if the command that produced it named both
> endpoints. `<tip>` alone is a history number wearing a range's clothing.

## Range identity — establish this first

```bash
BASE=v1.0.0 TIP=v1.1.0

# 1. Peel annotated tags. `git rev-parse v1.0.0` returns the TAG OBJECT sha,
#    not the commit it points at. Always ^{commit}.
git rev-parse "$BASE^{commit}" "$TIP^{commit}"

# 2. Commit counts — the range, and the history, side by side.
git rev-list --count "$BASE..$TIP" # the release
git rev-list --no-merges --count "$BASE..$TIP"
git rev-list --merges --count "$BASE..$TIP"
git rev-list --count "$TIP" # whole history behind the tag
git rev-list --count "$BASE"

# 3. Rename-aware diffstat. Without the limit git silently prints
#    "exhaustive rename detection skipped" and scores moves as add+delete.
git -c diff.renameLimit=3000 diff --shortstat "$BASE..$TIP"
git -c diff.renameLimit=3000 diff --shortstat "$BASE..$TIP" -- < subtree > /
```

### The arithmetic self-check

```
count(BASE) + count(BASE..TIP) == count(TIP)
```

If an inherited figure equals `count(TIP)`, it is a **history** count, not a
range count. Worked case: a prior pass published "591 commits (578 non-merge +
13 merge)" for `v1.0.0..v1.1.0`. Measured: the range held **432 (430 + 2)**;
159 + 432 = 591 — the 591 was every commit reachable from the tag. The identity
proves it rather than argues it. (The 578/13 sub-counts did not decompose 591
either — an inherited figure can be internally inconsistent as well as
wrong-by-method.)

## Per-claim verification

```bash
# Is this hash actually in the range?
git merge-base --is-ancestor <hash> "$TIP"  && echo reachable-from-tip
git merge-base --is-ancestor <hash> "$BASE" && echo "PRE-RANGE — not this release"

# What did it REALLY touch? (never trust the subject line)
git show <hash> --name-status --format=''
git show <hash> --stat | tail -3

# Did its effect survive to the tip?
git show "$TIP:path/to/file" | grep <the-claimed-value>
```

### The three-part test for a changelog claim

A changelog line is only true if **all three** hold. Most audits check the first
and stop.

1. **Exists** — the hash resolves (`git cat-file -t`).
2. **In range** — ancestor of tip, _not_ ancestor of base.
3. **Survives** — the change it describes is still the state at the tip.

Part 3 is where releases lie without meaning to. See pitfall 3.

## Pitfalls

Each of these produced a confidently wrong number before being measured.

1. **History count published as a range count.** Covered above. The most common
   inherited error, because `git rev-list --count <tip>` looks like a reasonable
   thing to have run. Apply the arithmetic self-check to every inherited count.

2. **A commit message can lie about its own diff.** A commit titled _"negate
   ste-code/extracted/ in .gitignore, add extraction feedback"_ had a
   `--name-status` of exactly one line: `A .agents/feedback/exchange.md`. It
   never touched `.gitignore`. The changelog inherited the falsehood by copying
   the subject verbatim. **Never let a subject line stand as evidence of scope
   or attribution — run `--name-status`.** When the message is wrong, find the
   commits that did do the work and re-attribute.

3. **A claim can be true mid-range and reversed before the tag.** A "Changed"
   headline read _"update default agent model to poolside/laguna-s-2.1:free"_
   and its commit was real and in-range — but four later commits in the _same
   range_ moved it to `tencent/hy3:free`, which is what the tag actually ships.
   Publishing the headline would have told readers the opposite of the truth.
   For any "we changed X to Y" claim, read the value at the tip:
   `git show "$TIP:<config>" | grep <key>`. Then reconstruct the ordering with
   `git log --reverse --format='%h %ad %s' --date=short "$BASE..$TIP" -- <path>`
   and describe the _net_ change, naming the intermediate only if it matters.

4. **Rename detection silently changes the totals.** Two passes over one range
   reported 2,622 files / +322,577 / −161,827 and 2,605 files / +319,500 /
   −158,750. Neither was wrong — the first hit git's rename limit and counted
   moved files as add+delete pairs. **Diagnostic signature: the insertion and
   deletion deltas are identical** (here ±3,077), because every unrecognised
   move adds and removes the same lines. A subtree containing no moved paths
   matched to the byte across both methods, confirming the diagnosis. Publish
   the rename-aware figure and state the flag, or it is not reproducible.
   Distinguish "wrong method" from "different setting" when correcting a
   predecessor — it changes how much else you re-check.

5. **`git rev-parse --short` takes one revision.** `git rev-parse --short=7 A B`
   fails with `fatal: Needed a single revision`. Loop, or drop `--short`.

6. **Counting by `git ls-tree` at two revs beats diffing.** For "how many X at
   each end", `git ls-tree <rev> <dir>/ | grep -c <pattern>` is cheap, exact and
   repeatable. Reserve full-range `git diff` for the one headline diffstat and
   run it **once** — it is the expensive call in an audit.

7. **A file's presence at both ends hides churn; absence at one end proves an
   addition.** To prove something is new in the range, test both endpoints
   explicitly rather than reading the log:
   `git cat-file -e "$BASE:path" 2>/dev/null && echo existed || echo new`.

8. **Migration ranges have a repair tail — read it as one event.** A
   `scripts/ → tools/` move was followed inside the same range by eight
   follow-up fixes (path depth across 28 scripts, CRLF/syntax, wrapper paths, a
   duplicate config file "created by path resolution bug", stale docstrings).
   Reporting nine independent items misrepresents the release; reporting "one
   move plus its repair tail" is both shorter and true.

9. **Date-stamp a feature by artifact existence at the rev, not by vocabulary.**
   When a later release's notes are available they contaminate earlier framing.
   Test at the tag:
   `git ls-tree -r --name-only "$TIP" <dir>/ | grep -iE '<pat>'`. A benchmark
   described in a sibling v1.2.0 note as a "five-colour harness" had, at the
   v1.1.0 tag, `adversarial.py`/`verification.py`/`black.py`/ `purple.py`
   present but **no** `red.py`, `blue.py`, `white.py` — so the later vocabulary
   was right for a different release. "No colours yet" would have been wrong
   too. Enumerate; don't generalise in either direction.

10. **Omission is a finding.** The audited range added three rules to a writing
    standard (51 → 54) and the changelog never stated the rule count anywhere,
    nor listed the two commits that added them. Nothing was false; the
    load-bearing fact was simply absent. Record these as **OMITTED** alongside
    verified/disputed — for a release, a missing headline is usually more
    consequential than a slightly wrong one.

11. **Automated version stampers define their own blind spot.** A commit titled
    _"stamp the version being released, not the previous tag"_ left the file it
    stamped internally inconsistent: blockquote fields updated to 1.1.0, while
    the H1, prose, an ASCII diagram and table rows still said 1.0.0. Cause was
    visible in the stamper's `registry.json` — it rewrites only
    registry-declared regex claim sites. Wherever a repo automates stamping,
    grep the _whole_ file for the old version, not just the managed fields.

## Reporting

Log incrementally — land range identity and the first block of findings before
finishing the sweep, so a long audit survives a timeout. Every number gets the
exact command that produced it; a figure without its command cannot be
re-verified by the next pass and will be re-litigated.

When correcting an inherited number, give the right value, the wrong one, **and
the method that produced the wrong one**. "591 was the history count" tells the
next agent how to avoid it; "591 is wrong" does not.

Close with a copy-pasteable safe-numbers block.

## Probe script

Save as `scripts/range-identity.sh` (read-only; never checks out or writes):

```bash
#!/usr/bin/env bash
# range-identity.sh <base> <tip> [subtree]
set -uo pipefail
BASE="${1:?usage: range-identity.sh <base> <tip> [subtree]}"
TIP="${2:?usage: range-identity.sh <base> <tip> [subtree]}"
SUB="${3:-}"
RENAME_LIMIT="${RENAME_LIMIT:-3000}"

echo "=== TAG -> COMMIT (peel annotated tags) ==="
BASE_SHA="$(git rev-parse "${BASE}^{commit}")" || exit 1
TIP_SHA="$(git rev-parse "${TIP}^{commit}")" || exit 1
printf '%-10s %s\n' "$BASE" "$BASE_SHA"
printf '%-10s %s\n' "$TIP" "$TIP_SHA"
for ref in "$BASE" "$TIP"; do
	[ "$(git cat-file -t "$ref" 2> /dev/null)" = "tag" ] \
		&& echo "  note: '$ref' is ANNOTATED — bare rev-parse returns the tag object"
done

echo
echo "=== COMMIT COUNTS ==="
R_ALL=$(git rev-list --count "$BASE..$TIP")
R_NOM=$(git rev-list --no-merges --count "$BASE..$TIP")
R_MRG=$(git rev-list --merges --count "$BASE..$TIP")
H_TIP=$(git rev-list --count "$TIP")
H_BAS=$(git rev-list --count "$BASE")
FP=$(git rev-list --count --first-parent "$BASE..$TIP")
printf 'range %s..%s : %s  (%s non-merge + %s merge)\n' "$BASE" "$TIP" "$R_ALL" "$R_NOM" "$R_MRG"
printf 'range first-parent : %s\n' "$FP"
printf 'history behind %-6s: %s\n' "$TIP" "$H_TIP"
printf 'history behind %-6s: %s\n' "$BASE" "$H_BAS"

echo
echo "--- self-check: count(base) + count(range) == count(tip) ---"
SUM=$((H_BAS + R_ALL))
if [ "$SUM" -eq "$H_TIP" ]; then
	echo "OK   $H_BAS + $R_ALL = $SUM = $H_TIP"
else echo "WARN $H_BAS + $R_ALL = $SUM != $H_TIP (shallow/grafted?)"; fi
echo "PUBLISH $R_ALL. An inherited figure equal to $H_TIP is a HISTORY count."

echo
echo "=== DIFFSTAT (renameLimit=$RENAME_LIMIT) ==="
echo -n "whole range : "
git -c diff.renameLimit="$RENAME_LIMIT" diff --shortstat "$BASE..$TIP" 2>&1 | tail -1
if [ -n "$SUB" ]; then
	echo -n "$SUB : "
	git -c diff.renameLimit="$RENAME_LIMIT" diff --shortstat "$BASE..$TIP" -- "$SUB" 2>&1 | tail -1
fi
echo "note: identical +/- deltas vs another pass == undetected renames, not disagreement."

echo
echo "=== TAGS INSIDE THE RANGE ==="
git tag --list --merged "$TIP" | while read -r t; do
	git merge-base --is-ancestor "$t" "$BASE" 2> /dev/null || echo "  $t"
done

echo
echo "=== SANITY: dirty tree? (audits must not commit) ==="
if [ -n "$(git status --porcelain)" ]; then
	echo "  DIRTY — other sessions may be writing here. Do not commit/tag/push."
	git status --porcelain | head -5
else echo "  clean"; fi
```

## Appendix — worked result, `0cf59e4..830d06c` (v1.0.0 → v1.1.0)

Second pass over a range a previous pass had measured. Findings log:
`.agents/tmp/research-findings-v1.1.0.md` (572 lines, 8 verified / 6 disputed).

**Identity.** Both tags annotated. Range **432 commits (430 + 2)**; first-parent
256; history behind tip 591, behind base 159. Inherited "591 (578+13)" was the
history count.

**Diffstat.** Whole range **2,605 files, +319,500 / −158,750** (rename-aware) vs
prior 2,622 / +322,577 / −161,827; `ste-code/` **1,061 files, +269,168 /
−98,217** matched exactly.

**Counts at each tag** (`git ls-tree`, no diff): rules 51 → **54**; +4 GR both
ends, so 55 → **58** units. Dictionary `##` entries 563 at both. Artifact tiers
6 → **9** (adds `_base`, `level-1`, `level-2`). `.agents/benchmark/` 35 files,
59 test cases across 14 categories. `.agents/scripts/` present → **absent**.

**Claims.** 16/16 cited hashes real, in-range, subjects matching — the changelog
invented nothing. Failures were in parts 2–3 of the three-part test: the model
headline was reversed before the tag (`deepseek-v4-pro` → poolside → **tencent/
hy3:free**, with `STE_MODEL` indirection the durable change), and `17b4f8d`'s
subject claimed a `.gitignore` edit it never made. Rule growth 55 → 58 was
OMITTED entirely.
