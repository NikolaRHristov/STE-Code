---
name: link-checking
description: Check markdown docs for broken links with lychee.
version: 1.0.0
tags: [lychee, links, documentation, qa, validation, markdown]
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

**An exclude that is too broad is worse than no check at all** — it silently
hides real breakage while reporting green. Every exclude must be narrow enough
that a genuine link of the same shape is still checked, and you must *prove*
that with a fixture rather than assert it.

Corollary: prefer excluding by *mechanism* (scheme, code-fence, fragment
policy) over excluding by *string match*. Mechanism excludes cannot over-match.

## Workflow

1. **Survey the link population before configuring.** Never write excludes
   blind. Dump and bucket first:
   ```sh
   lychee --dump --no-progress 'docs/**/*.md' \
     | sed -E 's#^(file://.*/)[^/]*$#\1<FILE>#' | sort | uniq -c | sort -rn
   ```
   The normalizing `sed` collapses per-file noise so the real *classes* of link
   (external, local relative, odd schemes) surface immediately. This single
   command tells you what your excludes must handle.

2. **Mine existing configs if reference repos are available.** Read every
   candidate before choosing; the best *config* and the best *runner* often
   live in different repos, so merge rather than copy one wholesale. Take only
   the tool in scope — resist importing a second scanner. Discard the source
   repo's project-specific ignore lists; they are noise elsewhere.
   See `references/config-mining.md`.

3. **Write the config.** See `references/lychee-config.md` for the key-by-key
   reference and the semantics that matter.

4. **Validate excludes with `--dump` before running.** `--dump` lists the links
   that *would* be checked, with no network traffic. If an intentionally-ignored
   pattern still appears, the exclude is wrong. Fast, free iteration.

5. **Prove exclude narrowness with a fixture.** Build a throwaway tree
   containing both a should-exclude case and a genuine same-shape link that must
   still be checked. Run `scripts/verify-linkcheck-config.sh`.

6. **Run for real and triage.** Separate findings into: genuinely broken,
   dead external host, and transient/not-yet-generated. Report file:line for
   each. Verify a suspicious timeout independently (`curl --max-time`, DNS
   lookup) before calling a host dead — distinguishes host outage from
   checker artifact.

7. **Leave known-but-unfixed findings VISIBLE.** When a real problem is found
   (e.g. a cited corpus was never vendored), do not add an exclude to silence
   it. Ship the exclude commented out with a note explaining how to enable it
   once triaged.

## Reporting findings

Group errors by root cause, not by file — 42 errors across 4 files is usually
3 causes. State each cause once, list affected locations under it, and mark
which are transient. Always give `file:line` from the report.

## Pitfalls

- **`--offline` drops all http(s) URLs, by design.** It checks local file links
  only. Never treat an offline run as the authoritative report, and if a
  verification step runs offline, **re-run online afterward** or the `latest`
  report is left misleadingly incomplete. An external URL "disappearing" under
  `--offline` is correct behavior, not a config bug.
- **Excludes are matched against the RESOLVED url**, not the raw markdown
  target. A repo-root-relative link resolves relative to the *file*, so
  `](ste-code/grouped/)` inside `ste-code/final/rules/x.md` becomes
  `.../ste-code/final/rules/ste-code/grouped/`. Anchor patterns to that
  mis-nested shape so the real path stays checked.
- **Omitting `file` from `scheme` silently skips every local link** while still
  exiting 0. If a repo is mostly internal links, this makes the check useless.
- **Single-quote globs** (`'docs/**/*.md'`) so the tool expands them, not the
  shell — otherwise `exclude_path` is applied inconsistently.
- **Exit code 2 means broken links; 1 means the tool failed.** Distinguish them
  in any runner, or a crash reads as a clean-but-broken result.
- **macOS has no `timeout(1)`.** Use the tool's own `timeout` config, or
  `curl --max-time` for one-off probes.
- **`grep -rIl` across a large repo hangs on `node_modules`.** Prune first:
  `--exclude-dir=node_modules --exclude-dir=.git --exclude-dir=target`, or
  `find … -prune`.
- **macOS system `python3` is 3.9 and has no `tomllib`.** Use the repo's
  `.venv/bin/python3` to validate TOML, or let the tool itself parse the config
  as the validity check.
- **Generated-content targets move under you.** File counts can change between
  runs while a pipeline writes. Re-check whether the error *count* held steady;
  if it did, findings are stable and only totals drift. Say so explicitly.
- **Check `git status` before claiming "not committed."** Repos can have
  auto-committers that sweep new files in. Report it rather than assume your
  own inaction held.
- **Add `.gitignore` for generated reports and the tool cache** in the same
  commit as the config, or the first run pollutes the repo.

## Support files

- `references/lychee-config.md` — lychee config key reference, semantics, exit codes.
- `references/config-mining.md` — how to compare/merge configs from reference repos.
- `scripts/verify-linkcheck-config.sh` — fixture harness proving excludes are narrow.
- `references/ste-code-setup.md` — the installed STE-Code setup and its baseline findings.
