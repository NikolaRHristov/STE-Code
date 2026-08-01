# Link Check (lychee)

Link checking for STE-Code markdown, using [lychee](https://github.com/lycheeverse/lychee).
Lychee is the **only** scanner used here — no markdown-link-check, no Vale, no alternates.

```
.agents/tools/linkcheck/
├── lychee.toml          # the configuration
├── run_linkcheck.sh     # runner (writes reports/)
├── README.md            # this file
└── reports/             # generated: <target>-<timestamp>.md + <target>-latest.md
```

## Usage

```sh
.agents/tools/linkcheck/run_linkcheck.sh              # final + artifacts
.agents/tools/linkcheck/run_linkcheck.sh final        # stable rule set only
.agents/tools/linkcheck/run_linkcheck.sh artifacts    # generated output only
.agents/tools/linkcheck/run_linkcheck.sh --offline    # local file links only, no network
.agents/tools/linkcheck/run_linkcheck.sh --no-cache final
.agents/tools/linkcheck/run_linkcheck.sh --suggest    # propose Wayback replacements
```

Exit codes: `0` clean, `1` lychee missing / bad usage, `2` broken links found.

Direct invocation works too:

```sh
lychee --config .agents/tools/linkcheck/lychee.toml 'ste-code/final/**/*.md'
```

## Provenance

Two local repos were mined for an existing lychee setup:

| Source | What it had | Taken? |
|---|---|---|
| `CodeEditorLand/WebSite/lychee.toml` | **Most advanced.** Cache + `max_cache_age`, retries with `retry_wait_time`, `max_redirects`, `include_fragments`, markdown report to file, `[header]` table, regex excludes with inline rationale | **Primary base** |
| `CodeEditorLand/Land/.lychee.toml` + `.lycheeignore` | Extension list, exclude/exclude_path, `accept` incl. 429 | `accept` list, exclude_path idea |
| `REPxREP/Repository/.lychee.toml` + `Maintain/Check/Links.sh` | Documented exclude blocks; wrapper script passing **single-quoted globs** so lychee (not the shell) expands them | **Runner script shape**, comment style |
| `REPxREP/Repository/Archive/lychee.toml` | Wide `accept` list, legacy `headers = [...]` array syntax | `accept` breadth only (legacy syntax rejected) |

Net: **CodeEditorLand/WebSite** had the most advanced *config*; **REPxREP** had the most advanced *invocation wrapper*. This setup merges both.

Deliberately **not** carried over: their project-specific ignore lists (shields.io, editor.land, Discord API, npmjs, Vite internals) and non-markdown extensions (`.rs`, `.ts`, `.tsx`, `.json`) — irrelevant to STE-Code.

## Configuration decisions

### Schemes — `["http", "https", "file"]`

`file` is **required**: most links in this repo are local relative markdown paths, and
dropping it would silently skip every internal link. Restricting the list also discards
documentation-only URIs such as `postgresql://db.internal:5432/app` that appear as
illustrative examples in rule files.

### `include_verbatim = false`

Fenced code blocks and inline code are **not** scanned. STE-Code rule files are full of
deliberately fake sample URLs (`https://api.example.com/v2/status`, `http://localhost:3000`,
`https://github.com/acme/widget-api.git`). Scanning them would drown real findings.

### `include_fragments = "none"`

Anchors are not validated. In this repo the section id lives in the link **text**
(`[master.md#sec9-rule9.3](ste-code/grouped/)`), never in the target, so fragment
checking would yield only false positives.

### Excludes

| Pattern | Why |
|---|---|
| `ste-code/(final\|artifacts)/.*ste-code/grouped/?$` | **The intentional backlinks.** Every generated rule file carries `> **Source:** [master.md#secN-ruleN.N](ste-code/grouped/)`. The link text is the real provenance pointer; the target is a repo-root-relative path that lychee resolves relative to the *file*, yielding `ste-code/final/rules/ste-code/grouped/`. Upstream `master.md` was removed, so these can never resolve. **47 in `final/`, ~235 in `artifacts/`.** The pattern is anchored to the mis-nested `ste-code/<x>/…/ste-code/grouped/` shape, so a genuine link to the real `ste-code/grouped/` directory is still checked. |
| `example.com` / `*.example.{com,org,net}` | RFC 2606 documentation placeholders. Defence in depth — most sit in code fences already skipped, but a few appear in prose tables. |
| `localhost`, `127.0.0.1`, `0.0.0.0`, `[::1]` | Local dev addresses in examples. |
| `mailto:`, `tel:` | Example contact URIs, not real endpoints. |
| `.agents/reference/` | **Commented out on purpose.** These are *real* findings — see below. |

`exclude_private` / `exclude_loopback` / `exclude_link_local` are enabled as a
network-level backstop for the same class of address.

### Accepted status codes

`200, 204, 206, 301, 302, 303, 307, 308, 403, 429` — `429` because GitHub rate-limits link
checkers and a 429 still proves the URL resolves; `403` because some CDNs reject
non-browser user agents. `host_concurrency = 4` and `host_request_interval = "100ms"`
keep us under GitHub's limits in the first place.

### Caching

`cache = true`, `max_cache_age = "1d"`, writing `.lycheecache` at the repo root.
`cache_exclude_status = ["429", "500..=599"]` so transient failures are never cached.

## Baseline results (2026-08-01, lychee 0.24.2)

### `ste-code/final/` — 65 markdown files (stable)

| | |
|---|---|
| Total links | 73 (26 unique) |
| Excluded | 51 (47 `grouped/` backlinks + placeholders) |
| Successful | 6 |
| **Errors** | **15** |
| **Timeouts** | **1** |

**All 15 errors are in one file — `ste-code/final/reference-catalogue.md`** — and all point at a
`.agents/reference/` corpus directory that does not exist anywhere in the repo:

```
reference-catalogue.md:8:42   .agents/reference/microsoft-writing-style-guide.md
reference-catalogue.md:9:64   .agents/reference/microsoft-style-guide-github.md
reference-catalogue.md:10:32  .agents/reference/google-style-guides.md
reference-catalogue.md:11:29  .agents/reference/kong-apiglossary.md
reference-catalogue.md:12:35  .agents/reference/dwyl-technical-glossary.txt
reference-catalogue.md:13:32  .agents/reference/jvalentino-glossary.md
reference-catalogue.md:14:37  .agents/reference/github-official-glossary.md
reference-catalogue.md:15:40  .agents/reference/devops-style-guide-glossary.md
reference-catalogue.md:16:37  .agents/reference/ryanwi-software-terms.txt
reference-catalogue.md:18:35  .agents/reference/en-wl-wordlist.md
reference-catalogue.md:19:41  .agents/reference/michaelwehar-5000-common.txt
reference-catalogue.md:22:24  .agents/reference/vale.md
reference-catalogue.md:23:32  .agents/reference/vale-microsoft.md
reference-catalogue.md:24:29  .agents/reference/vale-google.md
reference-catalogue.md:25:33  .agents/reference/vale-write-good.md
```

These are **genuine**, not config noise: the cited source corpora were never vendored.
Two fixes are possible — vendor the files into `.agents/reference/`, or make the catalogue
cite the upstream URLs directly. Until triaged, they stay visible. To silence them,
uncomment the `.agents/reference/` line in `lychee.toml`.

**Timeout:** `https://openste.org/` at `reference-catalogue.md:17:27`. Verified independently —
DNS resolves (`95.96.176.48`) but the host does not accept connections (`curl` times out at 45 s).
Host-side outage, not a checker artifact.

### `ste-code/artifacts/` — 102 markdown files (⚠ PARTIAL — regeneration in flight)

| | |
|---|---|
| Total links | 303 (56 unique) |
| Excluded | 252 |
| Successful | 6 |
| **Errors** | **42** |
| **Timeouts** | **3** |

> File count rose 88 → 93 → 102 across three runs in one session while the
> artifact pipeline was writing. Error count held steady at 42, so the findings
> below are stable; only the totals drift. Re-run after regeneration settles.

Errors by file:

| File | Count | Cause |
|---|---|---|
| `ste-code-rules.md` | 15 | `.agents/reference/*` (lines 40305–40322) — same root cause as `final/` |
| `_base/level4/07-catalogue.md` | 11 | `.agents/reference/*` (lines 10–21) |
| `_base/level5/07-catalogue.md` | 11 | `.agents/reference/*` (lines 10–21) |
| `README.md` | 5 | **Regeneration gap** — see below |

`ste-code/artifacts/README.md` advertises artifacts that have not been produced yet:

```
README.md:12:11  ste-code/artifacts/level1/system-prompt.txt
README.md:13:11  ste-code/artifacts/level2/system-prompt.txt
README.md:14:11  ste-code/artifacts/level3/system-prompt.txt
README.md:15:11  ste-code/artifacts/level4/system-prompt.txt
README.md:16:11  ste-code/artifacts/level5
```

Confirmed on disk: `level1/` and `level2/` hold only the numbered part files, `level3/` has one
file, and **`level4/` and `level5/` are empty**. No `system-prompt.txt` exists anywhere. These
five errors are expected to clear once the artifact pipeline finishes; **re-run this check
after regeneration completes** before treating them as defects.

**Timeouts:** `https://openste.org/` in `_base/level4/07-catalogue.md:19:27`,
`_base/level5/07-catalogue.md:19:27`, and `ste-code-rules.md:40314:27` — same dead host.

### Summary of real, actionable findings

1. `.agents/reference/` (15 files) is cited but never vendored — affects `final/` and `artifacts/`.
2. `https://openste.org/` is unreachable — 4 occurrences repo-wide.
3. `ste-code/artifacts/README.md` references five artifacts the pipeline has not yet emitted (transient).

No broken external links other than `openste.org`: all four `github.com/topics/*` links and both
`raw.githubusercontent.com` corpora resolve.
