---
name: link-checking
description:
    Find genuinely broken doc links without false-positive noise.
category: benchmark
capability: running-the-adversarial-benchmark
source: .agents/skills/validation/link-checking
layout: ste-code-canonical-v1
---

# Link Checking

Find genuinely broken links in a repo's documentation without drowning in false
positives from placeholder URLs, code samples, and intentional dangling
references.

## When to use

- "Check the docs for broken links" / "set up a link checker"
- Re-validating docs after a generator or pipeline rewrites markdown
- Auditing a docs site or README set before release
- Adapting an existing link-check config from another repo

## The governing principle

**An exclude that is too broad is worse than no check at all** - it silently
hides real breakage while reporting green. Every exclude must be narrow enough
that a genuine link of the same shape is still checked, and you must _prove_
that with a fixture rather than assert it.

Corollary: prefer excluding by _mechanism_ (scheme, code-fence, fragment policy)
over excluding by _string match_. Mechanism excludes cannot over-match.

## Workflow

1. **Survey the link population before configuring.** Never write excludes
   blind. Dump and bucket first:

    ```sh
    lychee --dump --no-progress 'docs/**/*.md' \
    	| sed -E 's#^(file://.*/)[^/]*$#\1<FILE>#' | sort | uniq -c | sort -rn
    ```

    The normalizing `sed` collapses per-file noise so the real _classes_ of link
    (external, local relative, odd schemes) surface immediately. This one
    command tells you what your excludes must handle.

2. **Mine existing configs if reference repos are available.** Read every
   candidate before choosing; the best _config_ and the best _runner_ often live
   in different repos, so merge rather than copy one wholesale. Take only the
   tool in scope - resist importing a second scanner. Discard the source repo's
   project-specific ignore lists; they are noise elsewhere. Record which repo
   contributed what, and say so in the final report.

3. **Write the config** (key reference below).

4. **Validate excludes with `--dump` before running.** `--dump` lists the links
   that _would_ be checked, with no network traffic. If an intentionally-ignored
   pattern still appears, the exclude is wrong. Fast, free iteration.

5. **Prove exclude narrowness with a fixture** (recipe below).

6. **Run for real and triage.** Separate findings into: genuinely broken, dead
   external host, and transient/not-yet-generated. Report file:line for each.
   Verify a suspicious timeout independently (`curl --max-time`, DNS lookup)
   before calling a host dead - distinguishes host outage from checker artifact.

7. **Leave known-but-unfixed findings VISIBLE.** When a real problem is found
   (e.g. a cited corpus was never vendored), do not add an exclude to silence
   it. Ship the exclude commented out with a note on how to enable it once
   triaged.

## Reporting findings

Group errors by root cause, not by file - 42 errors across 4 files is usually 3
causes. State each cause once, list affected locations under it, and mark which
are transient. Always give `file:line` from the report.

## Pitfalls

- **`--offline` drops all http(s) URLs, by design.** It checks local file links
  only. Never treat an offline run as the authoritative report, and if a
  verification step runs offline, **re-run online afterward** or the `latest`
  report is left misleadingly incomplete. An external URL "disappearing" under
  `--offline` is correct behavior, not a config bug.
- **Excludes match the RESOLVED url**, not the raw markdown target. A
  repo-root-relative link resolves relative to the _file_, so
  `](ste-code/grouped/)` inside `ste-code/final/rules/x.md` becomes
  `.../ste-code/final/rules/ste-code/grouped/`. Anchor patterns to that
  mis-nested shape so the real path stays checked.
- **Omitting `file` from `scheme` silently skips every local link** while still
  exiting 0. If a repo is mostly internal links, this makes the check useless.
- **Single-quote globs** (`'docs/**/*.md'`) so the tool expands them, not the
  shell - otherwise `exclude_path` is applied inconsistently.
- **Exit 2 = broken links; exit 1 = the tool failed.** Distinguish them in any
  runner, or a crash reads as a clean-but-broken result.
- **macOS has no `timeout(1)`.** Use the tool's own `timeout` config, or
  `curl --max-time` for one-off probes.
- **`grep -rIl` across a large repo hangs on `node_modules`.** Prune first:
  `--exclude-dir=node_modules --exclude-dir=.git --exclude-dir=target`.
- **macOS system `python3` is 3.9 and has no `tomllib`.** Use the repo's
  `.venv/bin/python3`, or let lychee parse the config as the validity check.
- **Generated-content targets move under you.** File counts can change between
  runs while a pipeline writes. Check whether the error _count_ held steady; if
  it did, findings are stable and only totals drift. Say so explicitly.
- **Check `git status` before claiming "not committed."** Repos can have
  auto-committers that sweep new files in. Report it rather than assume your own
  inaction held.
- **Add `.gitignore` for generated reports and the tool cache** alongside the
  config, or the first run pollutes the repo.

## lychee config reference (verified on 0.24.2)

Unknown keys are rejected at load, so the cheapest _schema_ validation is lychee
itself:

```sh
lychee --config lychee.toml --dump --offline some-file.md
# fail signals: "unknown field", "invalid type", "failed to parse"
```

| Key                                             | Value that matters        | Why                                                                                                                                         |
| ----------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `scheme`                                        | `["http","https","file"]` | `file` is **mandatory** for local links. Restricting the list is a mechanism-exclude dropping `postgresql://`-style doc URIs with no regex. |
| `include_verbatim`                              | `false`                   | Skips fenced/inline code - the biggest false-positive source in tutorial content.                                                           |
| `include_fragments`                             | `"none"`                  | Anchors false-positive when the section id lives in link _text_, or on JS-hydrated GitHub `#readme`/`#L123`.                                |
| `accept`                                        | add `403`, `429`          | 429 still proves the URL resolves; 403 is CDN UA-blocking.                                                                                  |
| `host_concurrency` / `host_request_interval`    | `4` / `"100ms"`           | Avoid the rate limit rather than accept it.                                                                                                 |
| `cache_exclude_status`                          | `["429","500..=599"]`     | Without it a transient failure is cached and re-reported stale.                                                                             |
| `exclude_private` / `_loopback` / `_link_local` | `true`                    | Mechanism excludes for RFC1918 - beats enumerating IP regexes.                                                                              |
| `[header]`                                      | **must be last**          | TOML tables swallow every scalar key after them. Legacy `headers = ["K=V"]` array syntax is rejected by 0.24.2.                             |

Exit codes: **0** clean · **1** lychee itself failed · **2** broken links found.

Flags worth knowing: `--dump` (links that would be checked, no network - best
exclude debugger), `--dump-inputs` (files that would be scanned - debugs globs),
`--suggest` (Wayback replacements), `--base` (resolve root-relative links
against a base dir; alternative to regexing mis-nested paths).

## Fixture recipe: proving an exclude is narrow

The load-bearing test. Build a tree with **both** the case that must be excluded
and a genuine same-shape link that must still be checked, then assert each
independently. Without the second case an over-broad exclude looks fine.

```sh
CFG=/path/to/lychee.toml
FIX=$(mktemp -d)
mkdir -p "$FIX/docs/rules" "$FIX/docs/grouped"
: > "$FIX/docs/grouped/g1.md"
cat > "$FIX/docs/rules/r.md" << 'MD'
> **Source:** [master.md#sec9](docs/grouped/)
[ph](https://api.example.com/x) [db](postgresql://h:5432/d)
[real](https://github.com/topics/word-list)
MD
printf 'Genuine [corpus](docs/grouped/).\n' > "$FIX/genuine.md"

D=$(cd "$FIX" && lychee --config "$CFG" --dump --offline 'docs/**/*.md' 'genuine.md')
O=$(cd "$FIX" && lychee --config "$CFG" --dump 'docs/**/*.md')

echo "$D" | grep -q 'rules/docs/grouped' && echo FAIL || echo "ok: backlink excluded"
echo "$D" | grep -qE 'file://.*[^s]/docs/grouped/?$' && echo "ok: genuine kept" || echo FAIL
echo "$D" | grep -q 'api.example.com' && echo FAIL || echo "ok: placeholder excluded"
echo "$O" | grep -q 'github.com/topics' && echo "ok: real URL kept" || echo FAIL
```

Assert external-URL retention against the **online** dump - under `--offline`
its absence is correct behavior, not a config bug.

Also assert that docs match the live report (error count, affected files)
whenever you hand-write numbers into a README; it catches doc drift.

## STE-Code: installed setup

Config + runner live in `.agents/tools/linkcheck/` (never under `ste-code/`):
`lychee.toml`, `run_linkcheck.sh` (args: `final` | `artifacts` | `all` |
`--offline` | `--no-cache` | `--suggest`), `README.md`, `reports/`.

Repo-specific decisions:

- ~47 provenance backlinks in `final/` (~235 in `artifacts/`) of the form
  `> **Source:** [master.md#secN-ruleN.N](ste-code/grouped/)` point at a removed
  upstream. Excluded via `ste-code/(final|artifacts)/.*ste-code/grouped/?$` -
  anchored to the mis-nested shape so the real `ste-code/grouped/` stays
  checked.
- `.agents/reference/` exclude ships **commented out**: the 15 cited corpora
  were genuinely never vendored, so the finding stays visible.
- `ste-code/artifacts/` is pipeline-generated and often partial - file counts
  drift mid-run. Re-run after regeneration settles before treating
  `artifacts/README.md` misses as defects.

Reference-repo provenance: config base from `<repo>/WebSite/lychee.toml`
(cache, retry, `[header]`, fragment policy); runner shape from
`<repo>/Repository/Maintain/Check/Links.sh` (quoted globs, tool-presence
guard).
