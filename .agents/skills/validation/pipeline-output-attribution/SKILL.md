---
name: pipeline-output-attribution
description: "Verify pipeline output matches its declared source."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [validation, attribution, displacement, monitoring, workers, pipeline, audit]
---

# Pipeline Output Attribution & Chain Monitoring

**Load this when**: auditing whether stage-N output really came from stage-N input,
chasing a "file looks fine but has the wrong content" bug, or monitoring background
worker chains that are rewriting files.

Two tightly-linked jobs in any multi-stage worker pipeline (extract → refine → merge → …):

1. **Attribution**: prove that output file `N` actually contains the content of input
   file `N`, and not some neighbour's. Well-formedness checks cannot catch this.
2. **Monitoring**: watch the background chains rewriting those files, and report
   status without touching the repo.

For STE-Code, the well-formedness checks (existence, content signals, truncation,
fabrication) live in the `ste-code-validate` skill. This skill is the *attribution*
layer on top of them, plus the watcher protocol. See "Overlap" at the bottom.

## 0. Rule zero: verify the metric before you act on it

**An audit bug does not merely mis-grade files — it manufactures phantom work.**

Real case: a handoff brief instructed a delegate to "repair EMPTY extracted sources,
e.g. `w055` contains only page headers and no table." The delegate's first move was to
re-check that claim. `w055` had **30 headwords**; it scored **93.3%**. *Zero* sources
needed repair. The entire "deeper blocker" in the brief was one under-matching regex,
and a downstream agent had been dispatched to fix data that was never broken.

So, in order:

1. Run the parser's `--selftest` (§5) — fixtures, not live data.
2. Re-derive the brief's headline claim yourself before executing on it.
3. Only then judge files, and only then repair anything.

A brief that says "X is empty/corrupt" is a **claim about a measurement**, not a fact
about the disk. Confirm it costs one command; acting on it costs a whole session.

## 1. The displacement failure mode

A file passes every quality gate — good size, clean tables, no truncation, no
fabrication — and is still **wrong**, because it holds the wrong source pages.
Typical signature: a constant offset (e.g. every refined file shifted ~2 files /
~8 pages from its extracted source), caused by an off-by-N in a batch index or a
worker reading the wrong slice of a manifest.

No single-file quality check can see this. You must compare **against the declared
source**.

## 2. The overlap metric

Pick a cheap, high-signal content key both sides share. For dictionary-style pages
that key is the **headword**:

```
overlap = |keys(output_N) ∩ keys(source_N)| / |keys(source_N)|
PASS at overlap >= 0.5
```

A correctly-attributed file scores 0.6–1.0. A displaced file scores ~0.0.
Threshold at 0.5 because refinement legitimately merges, reformats, and drops
boilerplate — exact equality is not expected.

The denominator is the **source**, deliberately: output may legitimately contain
*fewer* keys (merged continuation rows), but must never contain keys the source lacks.

Use the script in the Appendix rather than hand-typing regexes:

```bash
python3 /tmp/attribution_audit.py --selftest                    # ALWAYS first
python3 /tmp/attribution_audit.py --repo . --workers 054,055,056 --launch-ts 1785000000
python3 /tmp/attribution_audit.py --repo . --diagnose 082       # why is it low?
```

## 3. PITFALL: three headword-regex bugs (silent false negatives)

PDF-derived markdown is not uniform. Three distinct shapes each defeat a "reasonable"
regex, and each has produced a wrong verdict that was written into a state doc.

### 3a. Double leading pipe

An empty first column from the original PDF grid:

```
||**Word**<br>**(part of speech)**|**Approved meaning/**...
||**EACH (adj)**|Every one of two or more objects or persons...
```

`^\|\s*` cannot match `||**EACH (adj)**`. Fix: `^\|+`.
Measured impact: **10 of 35** audited sources were double-pipe; workers 055, 074, 082,
083 were recorded as "still displaced" when their true scores were 90.0/84.6/81.6/92.6%.

### 3b. Collapsed one-line tables — `^` anchoring itself is the bug

Fixing 3a is **not enough**. Some extractions emit an entire multi-row table on ONE
physical line:

```
||**Word**|**x**||---|---||**outside (adv)**|OUTDOORS|**over (prep)**|ABOVE|
```

Any `^`-anchored form — including the `^\|+` fix from 3a — matches at most the first
cell of that line. Verified on fixtures: anchored recovers **0** keys from a collapsed
line; non-anchored recovers all of them. On real data, `w080` scored **3** keys
anchored vs **29** non-anchored — reported as a 0.0% FAIL when it was actually 86.2%.

**Do not anchor at all:**

```python
ROW  = re.compile(r'\|\s*\*{0,2}\s*([A-Za-z][A-Za-z\-]*)\s*\*{0,2}\s*\(')   # no ^
HEAD = re.compile(r'^#{3,4}\s+\*{0,2}([A-Za-z][A-Za-z\-]*)\s*\(', re.M)
```

### 3c. Header furniture (the cost of de-anchoring)

De-anchoring newly matches table headers and page furniture as if they were headwords
(`**Word**<br>**(part of speech)**`, `Part`, `Page`, `Issue`). Filter them:

```python
STOP = {"part", "page", "word", "issue", "adj", "adv", "n", "v", "prep", "tn"}
keys = ({m.group(1).lower() for m in ROW.finditer(t)} |
        {m.group(1).lower() for m in HEAD.finditer(t)}) - STOP
```

**General lesson**: when a metric returns exactly 0.0 for a suspiciously round subset
of inputs, suspect the parser before you suspect the data. And when you fix a parser,
re-run the fixtures — 3a's fix silently left 3b in place for a whole session.

## 4. PITFALL: an empty denominator is not a failure

`0/0` is not 0%. Give it its own status so a parser bug can never masquerade as a
content failure:

```python
ov = (len(out_keys & src_keys) / len(src_keys)) if src_keys else -1.0
status = "PASS" if ov >= 0.5 else ("NODATA" if ov < 0 else "FAIL")
```

**If NODATA > 0, fix the parser before judging any file.** Do not publish a verdict
from a run that still contains NODATA rows. Note that a *genuinely* blank page (a
"Blank Page" spec filler) is also NODATA — distinguish "parser blind" from "page
really is empty" by eye before concluding either.

## 5. Fixture-selftest the parser (and expect your fixtures to be wrong)

Ship a `--selftest` mode that runs the parser against synthetic files covering every
known-bad shape (§3a–3c, blank page, overlap arithmetic). Run it before any audit whose
result will drive repair work. It costs a second and it is the only check that does not
depend on the data being sane.

**When a fixture assertion fails, do not assume the code is wrong.** Two of six
assertions failed on first run in a real session; investigation showed *both
expectations* were wrong and the parser's true behaviour was **stronger** than
predicted (it recovered 0 keys from a collapsed line where 1 was predicted, and
correctly declined to treat a split `**Word**<br>**(part of speech)**` header as a
headword). Fixing the expectations was correct. Confirm which side is wrong before
editing either.

## 6. PITFALL: never accept a "passed" signal from a command that did not run

A verification harness reported **passed** for a script invocation that exited 2 with
`can't open file … No such file or directory` — the script never executed. A green
status attached to a run that produced no output is not evidence of anything.

Before believing any verification result, confirm: non-zero output actually appeared,
the exit code is 0, and the assertions you expected are named in the output. If a
harness marks a non-run as passing, say so explicitly rather than inheriting the claim.

### Writing a scratch verification script (tempdir divergence)

Backends can resolve `TMPDIR` to **different filesystems**: a file written by one tool
may be invisible to the shell. `write_file` additionally refuses `/var/...` and other
system paths as "sensitive". Symptom: you write the script, then the runner cannot find
it (exit 2).

Reliable pattern — author inside the repo, then stage into the shell's own tempdir:

```bash
# 1. author with write_file -> <repo>/.agents/tmp/verify-stage.py
# 2. stage + run + clean up, all from the SAME shell:
TMPF="$(mktemp "${TMPDIR:-/tmp}/verify-XXXXXX")" && mv "$TMPF" "$TMPF.py" && TMPF="$TMPF.py"
cp .agents/tmp/verify-stage.py "$TMPF"
python3 "$TMPF"; RC=$?
rm -f "$TMPF" .agents/tmp/verify-stage.py
exit $RC
```

Print `os.path.realpath(__file__)` from the script so the log proves which copy ran,
and confirm both copies are gone afterward.

## 7. PITFALL: "not processed yet" is not "processed and still wrong"

While chains are actively rewriting files, compare each file's mtime to the chain
launch time. An old mtime means untouched — that is `STALE` (pending), not `FAIL`.
Conflating them inflates the failure count and invites redundant relaunches.

```python
fresh = os.path.getmtime(out_path) > LAUNCH_TS
status = "FAIL" if (ov < 0.5 and fresh) else "STALE"
```

Always print the mtime in the status table so the reader can audit this themselves.

## 8. Confirm a low score before believing it

Score the suspect output against **every** source file and print the top matches:

- Scores high against some *other* worker → **genuine displacement** (and you now
  know the exact offset).
- Scores ~0% against *all* of them → **parser bug**, not a content problem.

`--diagnose NNN` does exactly this. One command separates the two root causes;
skipping it is how the false verdicts above happened.

## 9. Read-only chain monitoring protocol

When assigned to watch chains another agent launched, the job is **report, not repair**.

1. **Touch no repo files.** Keep the monitor script and progress log out of the repo —
   but mind the tempdir divergence in §6; stage from the same shell that runs it.
   State the read-only guarantee explicitly in the final report.
2. **Liveness**: `ps -p <pid>` per chain. An exited chain is not automatically a
   failure — verify whether its batches completed before raising an alarm.
3. **Concurrency**: `pgrep -f <worker-wrapper> | wc -l`. Respect the documented
   ceiling (free tiers 429 above it) before launching anything yourself. Count only
   real workers: an interactive TUI or a monitor loop can inflate this.
4. **A chain that `exec`s keeps its PID but changes its argv.** A launcher ending in
   `exec python3 run_batch.py 31 6` still shows the original PID. Never conclude
   "the final batch never launched" from the PID alone — read the live args:
   ```bash
   ps -p <pid> -o args=
   ```
   To see which item a worker is on, grep the live argv for its prompt/---item file:
   ```bash
   ps -o command -p $(pgrep -f worker-wrapper | tr '\n' ',' | sed 's/,$//') \
     | grep -oE 'prompt-[0-9]+' | sort -u
   ```
5. **Poll, never block.** Long foreground waits get reaped. When polling with
   `sleep N && check`, set the tool timeout **greater than N** or the call dies before
   the check runs. Background loggers are fine; Hermes rejects `nohup`/`&`/`disown`
   in foreground mode — use `terminal(background=true)`.
6. **Report a trend, not a snapshot.** Counts over time, throughput, and an ETA:
   `PASS=22 FAIL=0 STALE=13, ~1.1 files/min, ETA 05:05`. A bare table is not actionable.
7. **Only intervene under the stated condition.** If the brief says "relaunch only if
   a chain died without completing its batches", verify *both* halves before acting.

### Do not launch work into a running chain's range

Batch runners commonly load their checkpoint **once at import** into a module-level
global:

```python
_checkpoint = _load_checkpoint()   # module scope — never re-read
```

A long-running chain therefore holds a **stale** copy: it cannot see completions
written by anyone else, and will redo that work and race you on the same output paths.
Before adding parallelism, check how the checkpoint is loaded. If it is import-time
global state, let the running chain finish its own range rather than launching
overlapping batches "to speed things up" — the redundant runs cost more than they save
and can corrupt output.

## 10. Report the metric bug louder than the content result

If the audit method you were handed is wrong, lead with that. A bad verdict already
written into a handoff/state doc keeps propagating until someone contradicts it.
Show **both** numbers side by side — as-specified and corrected — so the reader sees
precisely what changed and why:

```
wkr | status | anchored% | fixed% | mtime
055 | PASS   |    n/a    |  93.3  | 04:34:54
080 | PASS   |    0.0    |  86.2  | 05:12:03
```

`n/a` / `0.0` in the as-specified column is itself the evidence that the old regex was
blind to that file. Then recommend the exact one-line fix to the source doc — and if
the brief was read-only, recommend it rather than editing it.

Also report **what you did not touch**. If `git status` shows files modified by another
concurrent session (a sibling stage's output directory), flag them by name and mtime so
the committing agent does not sweep them in. Distinguish files a tool auto-committed on
your behalf from files you committed yourself.

## Overlap with ste-code-validate

`ste-code-validate` owns per-batch well-formedness (Checks 1-4: existence/size,
content signals, truncation, fabrication) and the validation-log lifecycle. This skill
owns attribution (a "Check 5") and the watcher protocol. If the two are ever merged,
this content belongs as "Check 5 + Monitoring" inside that skill.

**Known defect in that skill** (could not be patched from here — see authoring note):
its "Content Volume" check counts dictionary entries with

```bash
grep -c "^| \*\*" ste-code/extracted/w*-p*.md    # WRONG: anchored AND space after |
```

which fails on all three shapes in §3 and will under-count badly. Replace with the
non-anchored `ROW` regex above. Flag this to the user; do not rely on that check.

## Appendix: audit script

Write to `/tmp/attribution_audit.py` and run. Adjust `OUT_GLOB`/`SRC_GLOB` for other
pipelines. Kept inline (not under `scripts/`) because `skill_manage(write_file)` cannot
resolve this skill — see the authoring note.

```python
#!/usr/bin/env python3
"""Displacement audit: does output/rNNN actually contain source/wNNN's pages?

    overlap = |keys(output) & keys(source)| / |keys(source)|;  PASS at >= 0.5.

Guards four bugs that each produced a real false verdict on this pipeline:
  1. LEADING-PIPE      naive `^\|\s*` misses `||**EACH (adj)**|` rows.
  2. LINE-ANCHORING    `^\|+` still misses tables collapsed onto ONE physical line
                       (w080: anchored=3 keys, non-anchored=29). Do not anchor.
  3. HEADER FURNITURE  de-anchoring newly matches `**Word**|`, `Part`, `Page`. Use STOP.
  4. EMPTY DENOMINATOR 0/0 is not 0%. Report NODATA, never FAIL.

Also separates STALE (old mtime, not re-run) from FAIL (re-run, still wrong).
RUN --selftest BEFORE any run whose result will drive data repair.
"""
import argparse, datetime, glob, os, re, tempfile, time

# NOT anchored: extracted tables may collapse onto one physical line.
ROW = re.compile(r'\|\s*\*{0,2}\s*([A-Za-z][A-Za-z\-]*)\s*\*{0,2}\s*\(')
ROW_ANCHORED = re.compile(r'^\|+\s*\*{0,2}\s*([A-Za-z][A-Za-z\-]*)\s*\(', re.M)
HEAD = re.compile(r'^#{3,4}\s+\*{0,2}([A-Za-z][A-Za-z\-]*)\s*\(', re.M)
STOP = {"part", "page", "word", "issue", "adj", "adv", "n", "v", "prep", "tn"}

OUT_GLOB = "ste-code/refined/r{n}-*"
SRC_GLOB = "ste-code/extracted/w{n}-*"


def headwords(path, rowre=ROW):
    t = open(path, encoding='utf-8', errors='ignore').read()
    return ({m.group(1).lower() for m in rowre.finditer(t)} |
            {m.group(1).lower() for m in HEAD.finditer(t)}) - STOP


def first(pattern):
    hits = sorted(glob.glob(pattern))
    return hits[0] if hits else None


def audit(repo, workers, launch_ts):
    rows = []
    for n in workers:
        out = first(os.path.join(repo, OUT_GLOB.format(n=n)))
        src = first(os.path.join(repo, SRC_GLOB.format(n=n)))
        if not out or not src:
            rows.append((n, "MISSING", -1.0, -1.0, "-")); continue
        s_keys, o_keys = headwords(src), headwords(out)
        ov = (len(o_keys & s_keys) / len(s_keys)) if s_keys else -1.0
        s_a, o_a = headwords(src, ROW_ANCHORED), headwords(out, ROW_ANCHORED)
        anch = (len(o_a & s_a) / len(s_a)) if s_a else -1.0
        mt = os.path.getmtime(out)
        if ov < 0:           st = "NODATA"
        elif ov >= 0.5:      st = "PASS"
        elif mt > launch_ts: st = "FAIL"
        else:                st = "STALE"
        rows.append((n, st, anch * 100, ov * 100,
                     time.strftime("%H:%M:%S", time.localtime(mt))))
    return rows


def diagnose(repo, n):
    """Displaced file matches SOME other source; a parser bug matches none."""
    out = first(os.path.join(repo, OUT_GLOB.format(n=n)))
    if not out:
        print(f"no output file for {n}"); return
    o_keys = headwords(out)
    scores = []
    for src in sorted(glob.glob(os.path.join(repo, "ste-code/extracted/w*"))):
        s_keys = headwords(src)
        if s_keys:
            scores.append((len(o_keys & s_keys) / len(s_keys), os.path.basename(src)))
    scores.sort(reverse=True)
    print(f"r{n}: {len(o_keys)} keys, sample={sorted(o_keys)[:6]}")
    for pct, name in scores[:5]:
        print(f"   {pct * 100:5.1f}%  {name}")
    print("   -> matches NOTHING: suspect a parser bug, not displacement."
          if not scores or scores[0][0] < 0.1 else
          "   -> matches another worker: genuine displacement.")


def selftest():
    """Fixture-verify the parser against shapes that have actually bitten us."""
    tmp = tempfile.mkdtemp(prefix="attribution-selftest-"); fails = []

    def wf(name, body):
        p = os.path.join(tmp, name); open(p, "w", encoding="utf-8").write(body); return p

    def ck(label, got, want):
        ok = got == want
        print(("  PASS  " if ok else "  FAIL  ") + label)
        if not ok:
            print("          got =", got); print("          want=", want); fails.append(label)

    dp = wf("dp.md", "||**Word**<br>**(part of speech)**|**Approved**|\n||---|---|\n"
                     "||**EACH (adj)**|Every one|\n||**EARLY (adv)**|Before time|\n")
    ck("double-pipe rows parse", headwords(dp), {"each", "early"})

    col = wf("col.md", "||**Word**|**x**||---|---||**outside (adv)**|OUTDOORS|"
                       "**over (prep)**|ABOVE|\n")
    ck("collapsed one-line table parses", headwords(col), {"outside", "over"})
    ck("anchored FAILS on collapsed line (why we de-anchor)",
       headwords(col, ROW_ANCHORED), set())

    sp = wf("sp.md", "|**ABLE (adj)**|meaning|\n#### BOLT (n)\n### **CABLE (n)**\n")
    ck("single-pipe + h3/h4 parse", headwords(sp), {"able", "bolt", "cable"})

    noise = wf("noise.md", "||**Word**<br>**(part of speech)**|x|\n|**Part (n)**|y|\n"
                           "|**Page (n)**|z|\n|**VALVE (n)**|w|\n")
    ck("header furniture rejected", headwords(noise), {"valve"})

    emp = wf("emp.md", "# Page 429 of 434\n**Blank Page**\n")
    ck("blank page yields empty set", headwords(emp), set())

    src = wf("src.md", "|**AAA (n)**|x|\n|**BBB (n)**|x|\n|**CCC (n)**|x|\n|**DDD (n)**|x|\n")
    ref = wf("ref.md", "|**AAA (n)**|x|\n|**BBB (n)**|x|\n|**ZZZ (n)**|x|\n")
    hs, hr = headwords(src), headwords(ref)
    ck("overlap denominator is the SOURCE", round(len(hs & hr) / len(hs), 4), 0.5)

    for p in os.listdir(tmp): os.unlink(os.path.join(tmp, p))
    os.rmdir(tmp)
    print("\n" + ("SELFTEST PASSED" if not fails else "SELFTEST FAILURES: %s" % fails))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--workers", default="")
    ap.add_argument("--launch-ts", type=float,
                    default=datetime.datetime.now().timestamp() - 86400)
    ap.add_argument("--diagnose", default="")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest: raise SystemExit(selftest())
    if a.diagnose: diagnose(a.repo, a.diagnose); return

    workers = ([w.strip() for w in a.workers.split(",") if w.strip()] if a.workers
               else sorted({os.path.basename(p)[1:4]
                            for p in glob.glob(os.path.join(a.repo, "ste-code/refined/r*"))
                            if os.path.basename(p)[1:4].isdigit()}))

    rows = audit(a.repo, workers, a.launch_ts)
    t = {k: sum(1 for r in rows if r[1] == k)
         for k in ("PASS", "FAIL", "STALE", "NODATA", "MISSING")}
    print(f"=== {time.strftime('%H:%M:%S')} | PASS={t['PASS']} FAIL={t['FAIL']} "
          f"STALE={t['STALE']} NODATA={t['NODATA']} MISS={t['MISSING']} / {len(rows)} ===")
    print("wkr | status | anchored% | fixed% | mtime")
    for n, st, nv, fx, mt in rows:
        ns = "  n/a" if nv < 0 else f"{nv:5.1f}"
        fs = "  n/a" if fx < 0 else f"{fx:5.1f}"
        print(f"{n} | {st:6s} |   {ns}    | {fs}  | {mt}")
    if t["NODATA"]:
        print("\nNODATA present -> fix the parser BEFORE judging any file.")


if __name__ == "__main__":
    main()
```

## Authoring note (tooling quirk on this profile — reconfirmed)

`skill_manage` `patch` / `edit` / `write_file` return *"Skill not found in active
profile"* for skills that `skill_view` reads without trouble, including this one.
Reconfirmed in a later session: `write_file` for `scripts/attribution_audit.py` was
refused, which is why the script stays inline in the Appendix.

Only `action='create'` resolves. To update, re-issue `create` with the full updated
body — it overwrites. A genuine protection error reads "pinned" or "not
curator-managed", not "not found"; do not mistake this quirk for protection.

Note the profile layout is nested (`profiles/ste-code/profiles/ste-code/`), and
sibling skills such as `ste-code-validate` live under a directory whose name differs
from their frontmatter `name:`. That mismatch is the likely cause, and it means those
skills are effectively read-only from here — report defects in them rather than
attempting edits.
