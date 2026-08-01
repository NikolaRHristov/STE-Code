# Vale linter

> Source: https://github.com/errata-ai/vale
> Fetched by finalize reference fetcher.

---

[Skip to content](https://github.com/vale-cli/vale#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/vale-cli/vale) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/vale-cli/vale) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/vale-cli/vale) to refresh your session.Dismiss alert

{{ message }}

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/vale-cli/vale).

[vale-cli](https://github.com/vale-cli)/ **[vale](https://github.com/vale-cli/vale)** Public

- Sponsor







# Sponsor vale-cli/vale























##### GitHub Sponsors

[Learn more about Sponsors](https://github.com/sponsors)







[![@jdkato](https://avatars.githubusercontent.com/u/8785025?s=80&v=4)](https://github.com/jdkato)



[jdkato](https://github.com/jdkato)



[jdkato](https://github.com/jdkato)



[Sponsor](https://github.com/sponsors/jdkato)









##### External links





![open_collective](https://github.githubassets.com/assets/open_collective-0a706523753d.svg)



[opencollective.com/ **vale**](https://opencollective.com/vale)









[Learn more about funding links in repositories](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository).




[Report abuse](https://github.com/contact/report-abuse?report=vale-cli%2Fvale+%28Repository+Funding+Links%29)

- [Notifications](https://github.com/login?return_to=%2Fvale-cli%2Fvale) You must be signed in to change notification settings
- [Fork\\
208](https://github.com/login?return_to=%2Fvale-cli%2Fvale)
- [Star\\
5.7k](https://github.com/login?return_to=%2Fvale-cli%2Fvale)


v3

[**4** Branches](https://github.com/vale-cli/vale/branches) [**195** Tags](https://github.com/vale-cli/vale/tags)

[Go to Branches page](https://github.com/vale-cli/vale/branches)[Go to Tags page](https://github.com/vale-cli/vale/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![jdkato](https://avatars.githubusercontent.com/u/8785025?v=4&size=40)](https://github.com/jdkato)[jdkato](https://github.com/vale-cli/vale/commits?author=jdkato)<br>[Update SECURITY.md](https://github.com/vale-cli/vale/commit/72a15022b5a8ca541117c70a2b4e2004635e0f45)<br>success<br>4 hours agoJul 31, 2026<br>[72a1502](https://github.com/vale-cli/vale/commit/72a15022b5a8ca541117c70a2b4e2004635e0f45) · 4 hours agoJul 31, 2026<br>## History<br>[1,976 Commits](https://github.com/vale-cli/vale/commits/v3/) <br>Open commit details<br>[View commit history for this file.](https://github.com/vale-cli/vale/commits/v3/) 1,976 Commits |
| [.github](https://github.com/vale-cli/vale/tree/v3/.github ".github") | [.github](https://github.com/vale-cli/vale/tree/v3/.github ".github") | [docs: fix CI](https://github.com/vale-cli/vale/commit/fe71481c95665a2343d81874489f8b012442a377 "docs: fix CI  Signed-off-by: Joseph Kato <joseph@jdkato.io>") | 12 hours agoJul 31, 2026 |
| [.well-known](https://github.com/vale-cli/vale/tree/v3/.well-known ".well-known") | [.well-known](https://github.com/vale-cli/vale/tree/v3/.well-known ".well-known") | [chore: add `.well-known`](https://github.com/vale-cli/vale/commit/b0a597a6f17e8fd9cefd3d4c1d81a24ed3496a91 "chore: add `.well-known`  Signed-off-by: Joseph Kato <joseph@jdkato.io>") | last yearJun 6, 2025 |
| [cmd/vale](https://github.com/vale-cli/vale/tree/v3/cmd/vale "This path skips through empty directories") | [cmd/vale](https://github.com/vale-cli/vale/tree/v3/cmd/vale "This path skips through empty directories") | [fix: stop sharing per-file scope state across goroutines](https://github.com/vale-cli/vale/commit/ff6de4d5e3e44b30a1083a5f07e5ae566154e996 "fix: stop sharing per-file scope state across goroutines  Signed-off-by: Joseph Kato <joseph@jdkato.io>") | 13 hours agoJul 31, 2026 |
| [internal](https://github.com/vale-cli/vale/tree/v3/internal "internal") | [internal](https://github.com/vale-cli/vale/tree/v3/internal "internal") | [docs: fix old links](https://github.com/vale-cli/vale/commit/6d08e80baa20b53e135ee84777ed7a599257ac47 "docs: fix old links  Signed-off-by: Joseph Kato <joseph@jdkato.io>") | 7 hours agoJul 31, 2026 |
| [testdata](https://github.com/vale-cli/vale/tree/v3/testdata "testdata") | [testdata](https://github.com/vale-cli/vale/tree/v3/testdata "testdata") | [fix: stop narrowing paragraph to a scope nothing carries](https://github.com/vale-cli/vale/commit/769943cc13dc9d7ba8151e4f132bd61488f66492 "fix: stop narrowing paragraph to a scope nothing carries  A `sequence` rule declaring `scope: paragraph` matched nothing and said nothing. sentenceScope narrowed it to `sentence.paragraph`, and no block is ever built with that scope: doNLP produces `paragraph.<scope>` from splitting and `sentence.<scope>` from segmentation, and the two families never cross. `list` and `heading` worked because those are block scope names; `paragraph` is not one.  It names no block of its own because splitting wraps every block as `paragraph.<scope>` -- headings and list items included -- so the scope already describes what an undeclared one does. An `existence` rule scoped to `paragraph` reports headings and list items today. Narrowing it any further asks for something that was never built.  So `paragraph` is left as `sentence`, and `paragraph.md` as `sentence.md`. A scope that merely starts with the word, such as `paragraphs`, is untouched.  This restores a result for the scope rather than the result 3.16.0 gave. That build reported the paragraph alone because a sequence rule reached paragraphs and nothing else, which is the bug #1124 fixed -- the scope name happened to agree with it.  Closes #1126.  Signed-off-by: Joseph Kato <joseph@jdkato.io>") | yesterdayJul 30, 2026 |
| [.gitattributes](https://github.com/vale-cli/vale/blob/v3/.gitattributes ".gitattributes") | [.gitattributes](https://github.com/vale-cli/vale/blob/v3/.gitattributes ".gitattributes") | [chore: mark fixtures as vendored](https://github.com/vale-cli/vale/commit/5a6e2708973ca836ca685598912e3d365a8fed8d "chore: mark fixtures as vendored") | 4 years agoJun 11, 2022 |
| [.gitignore](https://github.com/vale-cli/vale/blob/v3/.gitignore ".gitignore") | [.gitignore](https://github.com/vale-cli/vale/blob/v3/.gitignore ".gitignore") | [chore: update vulnerable go dependencies (](https://github.com/vale-cli/vale/commit/e73f5cdcde38dd5ee35243f417ad7abf653cd127 "chore: update vulnerable go dependencies (#938)  * upgrade  * upgrade  * revert gems  * revert  * upgrade to the latest vers  * revert  * revert  * partial upgrade  * revert partial upgrade  * archiver (depr) -> archive/zip  * ignore DS_Store  * remove unused ref  * revert unneeded upgrades  * run go mod tidy  * make code more robust  * upgrade testify and sprig  * more upgrades  * more upgrades  * more upgrades  * upgrade pterm  * revert  * test upgrading certain modules only  * expr upgrade  * upgrade copy  * upgrade godirwalk  * downgrade godirwalk, upgrade others  * change expr  * revert yaml  * fix pterm and godirwalk vers  * downgrade godirwalk  * upgrade back godirwalk  * go mod tidy  * remove godirwalk entirely and use filepath instead  * minor upgrades  * check os.MkdirAll  * no redeclaring err  * mkdirall -> mkdir  * ran goimport  * simplify syntax  * redeclare error to satisfy linting req  * fix err shadowing  * path traversal  * remove path traversal  * try mholt archives  * remove unused zip dep  * remove linkErr shadowing  * run goimport  * rename unused context as _  * revert to archive again  * file traversal error remove  * limit decompression size  * increase copy size  * revert filepath join  * change filepath, revert io copy  * add limit reader  * change to 10 GB size limit  * change to CopyN  * revert back to Copy  * go mod tidy") [#938](https://github.com/vale-cli/vale/pull/938) [)](https://github.com/vale-cli/vale/commit/e73f5cdcde38dd5ee35243f417ad7abf653cd127 "chore: update vulnerable go dependencies (#938)  * upgrade  * upgrade  * revert gems  * revert  * upgrade to the latest vers  * revert  * revert  * partial upgrade  * revert partial upgrade  * archiver (depr) -> archive/zip  * ignore DS_Store  * remove unused ref  * revert unneeded upgrades  * run go mod tidy  * make code more robust  * upgrade testify and sprig  * more upgrades  * more upgrades  * more upgrades  * upgrade pterm  * revert  * test upgrading certain modules only  * expr upgrade  * upgrade copy  * upgrade godirwalk  * downgrade godirwalk, upgrade others  * change expr  * revert yaml  * fix pterm and godirwalk vers  * downgrade godirwalk  * upgrade back godirwalk  * go mod tidy  * remove godirwalk entirely and use filepath instead  * minor upgrades  * check os.MkdirAll  * no redeclaring err  * mkdirall -> mkdir  * ran goimport  * simplify syntax  * redeclare error to satisfy linting req  * fix err shadowing  * path traversal  * remove path traversal  * try mholt archives  * remove unused zip dep  * remove linkErr shadowing  * run goimport  * rename unused context as _  * revert to archive again  * file traversal error remove  * limit decompression size  * increase copy size  * revert filepath join  * change filepath, revert io copy  * add limit reader  * change to 10 GB size limit  * change to CopyN  * revert back to Copy  * go mod tidy") | last yearJan 13, 2025 |
| [.golangci.yml](https://github.com/vale-cli/vale/blob/v3/.golangci.yml ".golangci.yml") | [.golangci.yml](https://github.com/vale-cli/vale/blob/v3/.golangci.yml ".golangci.yml") | [chore: update golangci](https://github.com/vale-cli/vale/commit/dd6bc2686014377ba12726246a64a1e98cbe60f3 "chore: update golangci") | 10 months agoOct 22, 2025 |
| [.goreleaser.yml](https://github.com/vale-cli/vale/blob/v3/.goreleaser.yml ".goreleaser.yml") | [.goreleaser.yml](https://github.com/vale-cli/vale/blob/v3/.goreleaser.yml ".goreleaser.yml") | [chore: support immutable releases](https://github.com/vale-cli/vale/commit/8c4ed0df90e45f93818ffed5ba587ff1e220a142 "chore: support immutable releases  Signed-off-by: Joseph Kato <joseph@jdkato.io>") | 2 months agoJun 12, 2026 |
| [.pre-commit-hooks.yaml](https://github.com/vale-cli/vale/blob/v3/.pre-commit-hooks.yaml ".pre-commit-hooks.yaml") | [.pre-commit-hooks.yaml](https://github.com/vale-cli/vale/blob/v3/.pre-commit-hooks.yaml ".pre-commit-hooks.yaml") | [feat: Add pre-commit support (](https://github.com/vale-cli/vale/commit/16d3a7f19d37450770cf404e10ca303cc0d03585 "feat: Add pre-commit support (#558)") [#558](https://github.com/vale-cli/vale/pull/558) [)](https://github.com/vale-cli/vale/commit/16d3a7f19d37450770cf404e10ca303cc0d03585 "feat: Add pre-commit support (#558)") | 3 years agoJan 29, 2023 |
| [.vale.ini](https://github.com/vale-cli/vale/blob/v3/.vale.ini ".vale.ini") | [.vale.ini](https://github.com/vale-cli/vale/blob/v3/.vale.ini ".vale.ini") | [chore: update .vale.ini](https://github.com/vale-cli/vale/commit/e32b21d6d8ac56acd906b8804c26ae5c27e5a9ad "chore: update .vale.ini") | last yearMar 19, 2025 |
| [Dockerfile](https://github.com/vale-cli/vale/blob/v3/Dockerfile "Dockerfile") | [Dockerfile](https://github.com/vale-cli/vale/blob/v3/Dockerfile "Dockerfile") | [chore: bump Go version in Docker](https://github.com/vale-cli/vale/commit/c36307aef2cb84152629de07dfd1eca6d773fee8 "chore: bump Go version in Docker") | 8 months agoDec 3, 2025 |
| [LICENSE](https://github.com/vale-cli/vale/blob/v3/LICENSE "LICENSE") | [LICENSE](https://github.com/vale-cli/vale/blob/v3/LICENSE "LICENSE") | [docs: update year](https://github.com/vale-cli/vale/commit/d85cd19916f7e1c96d0924bc4bde018e18601c25 "docs: update year") | 4 years agoDec 12, 2022 |

[... middle omitted — see footer ...]


- **Easy-to-install**, stand-alone binaries: Unlike other tools, Vale doesn't require you to install and configure a particular programming language and its related tooling (such as Python/pip or Node.js/npm).


See the [documentation](https://vale.sh/) for more information.

## 🔍 At a Glance: Vale vs. `<...>`

[Permalink: :mag: At a Glance: Vale vs. <...>](https://github.com/vale-cli/vale#mag-at-a-glance-vale-vs-)

> **NOTE**: While all of the options listed below are open-source (CLI-based) linters for prose, their implementations and features vary significantly. And so, the "best" option will depends on your specific needs and preferences.

### Functionality

[Permalink: Functionality](https://github.com/vale-cli/vale#functionality)

| Tool | Extensible | Checks | Supports Markup | Built With | License |
| --- | --- | --- | --- | --- | --- |
| Vale | Yes (via YAML) | spelling, style | Yes (Markdown, AsciiDoc, reStructuredText, HTML, XML, Org) | Go | MIT |
| textlint | Yes (via JavaScript) | spelling, style | Yes (Markdown, AsciiDoc, reStructuredText, HTML, Re:VIEW) | JavaScript | MIT |
| RedPen | Yes (via Java) | spelling, style | Yes (Markdown, AsciiDoc, reStructuredText, Textile, Re:VIEW, and LaTeX) | Java | Apache-2.0 |
| write-good | Yes (via JavaScript) | style | No | JavaScript | MIT |
| proselint | No | style | No | Python | BSD 3-Clause |
| Joblint | No | style | No | JavaScript | MIT |
| alex | No | style | Yes (Markdown) | JavaScript | MIT |

The exact definition of "Supports Markup" varies by tool but, in general, it means that the format is understood at a higher level than a regular plain-text file (for example, features like excluding code blocks from spell check).

Extensibility means that there's a built-in means of creating your own rules without modifying the original source code.

### Benchmarks

[Permalink: Benchmarks](https://github.com/vale-cli/vale#benchmarks)

|     |     |
| --- | --- |
| ![](https://user-images.githubusercontent.com/8785025/97052257-809aa300-1535-11eb-83cd-65a52b29d6de.png) | ![](https://user-images.githubusercontent.com/8785025/97051175-91e2b000-1533-11eb-9a57-9d44d6def4c3.png) |
| This benchmark has all three tools configured to use their implementations of the `write-good` rule set and Unix-style output. | This benchmark runs Vale's implementation of `proselint`'s rule set against the original. Both tools are configured to use JSON output. |
| ![](https://user-images.githubusercontent.com/8785025/97053402-c5bfd480-1537-11eb-815b-a33ab13a59cf.png) | ![](https://user-images.githubusercontent.com/8785025/97055850-7b8d2200-153c-11eb-86fa-d882ce6babf8.png) |
| This benchmark runs Vale's implementation of Joblint's rule set against the original. Both tools are configured to use JSON output. | This benchmark has all three tools configured to perform only English spell checking using their default output styles. |

All benchmarking was performed using the open-source [hyperfine](https://github.com/sharkdp/hyperfine) tool on a MacBook Pro (2.9 GHz Intel Core i7):

```
hyperfine --warmup 3 '<command>'
```

The corpus IDs in the above plots—`gitlab` and `ydkjs`—correspond to the following files:

- A [snapshot](https://gitlab.com/gitlab-org/gitlab/-/tree/7d6a4025a0346f1f50d2825c85742e5a27b39a8b/doc) of GitLab's open-source documentation (1,500 Markdown files).

- A [chapter](https://raw.githubusercontent.com/getify/You-Dont-Know-JS/1st-ed/es6%20%26%20beyond/ch2.md) from the open-source book _You Don't Know JS_.


## About

📝 A markup-aware linter for prose built with speed and extensibility in mind.

[vale.sh](https://vale.sh/)

### Topics

[linter](https://github.com/topics/linter) [linting](https://github.com/topics/linting) [vale](https://github.com/topics/vale)

### Resources

[Readme](https://github.com/vale-cli/vale#readme-ov-file)

[MIT license](https://github.com/vale-cli/vale#MIT-1-ov-file)

### Code of conduct

[Code of conduct](https://github.com/vale-cli/vale#coc-ov-file)

### Contributing

[Contributing](https://github.com/vale-cli/vale#contributing-ov-file)

### Security policy

[Security policy](https://github.com/vale-cli/vale#security-ov-file)

[Activity](https://github.com/vale-cli/vale/activity)

[Custom properties](https://github.com/vale-cli/vale/custom-properties)

### Stars

[**5.7k** stars](https://github.com/vale-cli/vale/stargazers)

### Watchers

[**28** watching](https://github.com/vale-cli/vale/watchers)

### Forks

[**208** forks](https://github.com/vale-cli/vale/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fvale-cli%2Fvale&report=vale-cli+%28user%29)

## Releases

## Sponsor this project

## Used by

## Contributors

## Languages

You can’t perform that action at this time.

──────── [TRUNCATED] ────────
Showing 11,867 chars (head) + 4,793 chars (tail) of 28,192 total clean characters.
Full text saved to: /Users/nikola/.hermes/profiles/ste-code/cache/web/github.com-e1302a9cf1.md
To read the omitted middle: read_file path="/Users/nikola/.hermes/profiles/ste-code/cache/web/github.com-e1302a9cf1.md" offset=141 limit=200  (the file is the complete page; raise/lower offset to page through it).
─────────────────────────────