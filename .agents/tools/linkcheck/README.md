# Link Check

## Purpose

This unit checks every markdown link in the STE-Code corpus with
[lychee](https://github.com/lycheeverse/lychee). Lychee is the only scanner used
here — no markdown-link-check, no Vale, no alternates. Maintainers read this
file to run a check, to understand why a given class of link is excluded, and to
tell a genuine broken link from a deliberate placeholder.

## Footprint

This unit has no `config.yaml`; its settings live in `lychee.toml`.

- Reads: `.agents/tools/linkcheck/lychee.toml`, `ste-code/final/**/*.md`,
  `ste-code/artifacts/**/*.md`.
- Writes: `.agents/tools/linkcheck/reports/<target>-<timestamp>.md` and
  `.agents/tools/linkcheck/reports/<target>-latest.md`; the `.lycheecache` file
  at the repo root.

```
.agents/tools/linkcheck/
├── lychee.toml          # the configuration
├── run_linkcheck.sh     # runner (writes reports/)
├── README.md            # this file
└── reports/             # generated: <target>-<timestamp>.md + <target>-latest.md
```

## Usage

    .agents/tools/linkcheck/run_linkcheck.sh              # final + artifacts
    .agents/tools/linkcheck/run_linkcheck.sh final        # stable rule set only
    .agents/tools/linkcheck/run_linkcheck.sh artifacts    # generated output only
    .agents/tools/linkcheck/run_linkcheck.sh --offline    # local file links only
    .agents/tools/linkcheck/run_linkcheck.sh --no-cache final
    .agents/tools/linkcheck/run_linkcheck.sh --suggest    # propose Wayback URLs

Direct invocation works too:

    lychee --config .agents/tools/linkcheck/lychee.toml 'ste-code/final/**/*.md'

Exit codes: `0` clean, `1` lychee missing or bad usage, `2` broken links found.

## Behaviour

- The runner passes single-quoted globs so lychee expands them, not the shell.
- Schemes are limited to `http`, `https` and `file`.
- Fenced and inline code is skipped, so sample URLs in rule files never
  register.
- Fragments are not validated.
- Excluded patterns are dropped before any network call; remaining links are
  requested with capped host concurrency.
- Each run writes a timestamped markdown report and refreshes
  `<target>-latest.md`.

## Configuration

All knobs live in `lychee.toml`. None is hardcoded in the runner.

### Schemes — `["http", "https", "file"]`

`file` is required: most links in this repo are local relative markdown paths,
and dropping it would silently skip every internal link. Restricting the list
also discards documentation-only URIs such as
`postgresql://db.internal:5432/app` that appear as illustrative examples in rule
files.

### `include_verbatim = false`

Fenced code blocks and inline code are not scanned. STE-Code rule files are full
of deliberately fake sample URLs (`https://api.example.com/v2/status`,
`http://localhost:3000`, `https://github.com/acme/widget-api.git`). Scanning
them would drown real findings.

### `include_fragments = "none"`

Anchors are not validated. In this repo the section id lives in the link text
(`[master.md#sec9-rule9.3](ste-code/grouped/)`), never in the target, so
fragment checking would yield only false positives.

### Excludes

| Pattern                                             | Why                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ste-code/(final\|artifacts)/.*ste-code/grouped/?$` | The intentional backlinks. Every generated rule file carries `> **Source:** [master.md#secN-ruleN.N](ste-code/grouped/)`. The link text is the real provenance pointer; the target is a repo-root-relative path that lychee resolves relative to the _file_, yielding `ste-code/final/rules/ste-code/grouped/`. Upstream `master.md` was removed, so these can never resolve. The pattern is anchored to the mis-nested shape, so a genuine link to the real `ste-code/grouped/` directory is still checked. |
| `example.com` / `*.example.{com,org,net}`           | RFC 2606 documentation placeholders. Defence in depth — most sit in code fences already skipped, but a few appear in prose tables.                                                                                                                                                                                                                                                                                                                                                                           |
| `localhost`, `127.0.0.1`, `0.0.0.0`, `[::1]`        | Local dev addresses in examples.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `mailto:`, `tel:`                                   | Example contact URIs, not real endpoints.                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `.agents/reference/`                                | Commented out on purpose. These are real findings — see below.                                                                                                                                                                                                                                                                                                                                                                                                                                               |

`exclude_private`, `exclude_loopback` and `exclude_link_local` are enabled as a
network-level backstop for the same class of address.

### Accepted status codes

`200, 204, 206, 301, 302, 303, 307, 308, 403, 429` — `429` because GitHub
rate-limits link checkers and a 429 still proves the URL resolves; `403` because
some CDNs reject non-browser user agents. `host_concurrency = 4` and
`host_request_interval = "100ms"` keep the run under GitHub's limits in the
first place.

### Caching

`cache = true`, `max_cache_age = "1d"`, writing `.lycheecache` at the repo root.
`cache_exclude_status = ["429", "500..=599"]` so transient failures are never
cached.

## Failure modes

- **Exit 2** — broken links found. Read `reports/<target>-latest.md` before
  assuming a defect; compare against the known findings below.
- **Exit 1** — lychee is not installed or the target argument is unrecognised.
- **HTTP 429** — accepted as success, because a rate-limited response still
  proves the URL resolves. It is excluded from the cache so the next run
  re-checks it.
- **Stale cache** — a link fixed within the last day still reports broken. Rerun
  with `--no-cache`.
- **Moving target** — running against `ste-code/artifacts/` while the artifact
  pipeline writes produces drifting file counts. Re-run after regeneration
  settles.
- **Dead host timeouts** — an unreachable host consumes the full timeout per
  occurrence and slows the run.

## Known findings

Baseline recorded 2026-08-01 with lychee 0.24.2. Re-run before citing these
numbers.

1. `.agents/reference/` — 15 corpus files are cited by
   `ste-code/final/reference-catalogue.md` and by the level 4/5 catalogue
   sections, but were never vendored. Two fixes are possible: vendor the files,
   or make the catalogue cite upstream URLs directly. Until triaged they stay
   visible. To silence them, uncomment the `.agents/reference/` line in
   `lychee.toml`.
2. `https://openste.org/` — unreachable, 4 occurrences repo-wide. DNS resolves
   but the host refuses connections. Host-side outage, not a checker artifact.
3. `ste-code/artifacts/README.md` — advertises level 1-5 `system-prompt.txt`
   files the pipeline had not yet emitted. Transient; re-check after
   regeneration.

No broken external links other than `openste.org`: the `github.com/topics/*`
links and both `raw.githubusercontent.com` corpora resolve.

## Provenance

Two local repos were mined for an existing lychee setup.

| Source                                                        | What it had                                                                                                                                                                                   | Taken?                             |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `<repo>/WebSite/lychee.toml`                          | Most advanced. Cache + `max_cache_age`, retries with `retry_wait_time`, `max_redirects`, `include_fragments`, markdown report to file, `[header]` table, regex excludes with inline rationale | Primary base                       |
| `<repo>/Land/.lychee.toml` + `.lycheeignore`          | Extension list, exclude/exclude_path, `accept` incl. 429                                                                                                                                      | `accept` list, exclude_path idea   |
| `<repo>/Repository/.lychee.toml` + `Maintain/Check/Links.sh` | Documented exclude blocks; wrapper script passing single-quoted globs so lychee expands them                                                                                                  | Runner script shape, comment style |
| `<repo>/Repository/Archive/lychee.toml`                      | Wide `accept` list, legacy `headers = [...]` array syntax                                                                                                                                     | `accept` breadth only              |

Deliberately not carried over: project-specific ignore lists and non-markdown
extensions, which are irrelevant to STE-Code.

## See also

- [lychee.toml](lychee.toml) — the configuration
- [run_linkcheck.sh](run_linkcheck.sh) — the runner
- [../README.md](../README.md) — tools directory overview
