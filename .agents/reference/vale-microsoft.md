# errata-ai/Microsoft

> Source: https://github.com/errata-ai/Microsoft
> Fetched by finalize reference fetcher.

---

[Skip to content](https://github.com/vale-cli/Microsoft#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/vale-cli/Microsoft) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/vale-cli/Microsoft) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/vale-cli/Microsoft) to refresh your session.Dismiss alert

{{ message }}

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/vale-cli/Microsoft).

[vale-cli](https://github.com/vale-cli)/ **[Microsoft](https://github.com/vale-cli/Microsoft)** Public

- Sponsor







# Sponsor vale-cli/Microsoft























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




[Report abuse](https://github.com/contact/report-abuse?report=vale-cli%2FMicrosoft+%28Repository+Funding+Links%29)

- [Notifications](https://github.com/login?return_to=%2Fvale-cli%2FMicrosoft) You must be signed in to change notification settings
- [Fork\\
55](https://github.com/login?return_to=%2Fvale-cli%2FMicrosoft)
- [Star\\
110](https://github.com/login?return_to=%2Fvale-cli%2FMicrosoft)


master

[**1** Branch](https://github.com/vale-cli/Microsoft/branches) [**29** Tags](https://github.com/vale-cli/Microsoft/tags)

[Go to Branches page](https://github.com/vale-cli/Microsoft/branches)[Go to Tags page](https://github.com/vale-cli/Microsoft/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>[![jdkato](https://avatars.githubusercontent.com/u/8785025?v=4&size=40)](https://github.com/jdkato)[jdkato](https://github.com/vale-cli/Microsoft/commits?author=jdkato)<br>[Narrow the FirstPerson match to the pronoun itself](https://github.com/vale-cli/Microsoft/commit/7a9a1217a2924a4d58bfdcbefae813ff9113b6b9)<br>Open commit detailssuccess<br>2 days agoJul 30, 2026<br>[7a9a121](https://github.com/vale-cli/Microsoft/commit/7a9a1217a2924a4d58bfdcbefae813ff9113b6b9) · 2 days agoJul 30, 2026<br>## History<br>[196 Commits](https://github.com/vale-cli/Microsoft/commits/master/) <br>Open commit details<br>[View commit history for this file.](https://github.com/vale-cli/Microsoft/commits/master/) 196 Commits |
| [.github/workflows](https://github.com/vale-cli/Microsoft/tree/master/.github/workflows "This path skips through empty directories") | [.github/workflows](https://github.com/vale-cli/Microsoft/tree/master/.github/workflows "This path skips through empty directories") | [Update to Go tests and general refresh](https://github.com/vale-cli/Microsoft/commit/414362a553597e72fff7d7448404871bfd1c698f "Update to Go tests and general refresh") | 2 days agoJul 30, 2026 |
| [Microsoft](https://github.com/vale-cli/Microsoft/tree/master/Microsoft "Microsoft") | [Microsoft](https://github.com/vale-cli/Microsoft/tree/master/Microsoft "Microsoft") | [Narrow the FirstPerson match to the pronoun itself](https://github.com/vale-cli/Microsoft/commit/7a9a1217a2924a4d58bfdcbefae813ff9113b6b9 "Narrow the FirstPerson match to the pronoun itself  PR #72 reports bad underlines in editors using the language server and proposes removing `nonword: true`. The diagnosis is right, the change isn't sufficient: the token consumes the leading space, so mid-sentence \"Yesterday I walked\" matches \" I\" and the alert covers one character too many, reading \"such as ' I'\". Removing `nonword` leaves that unchanged.  Using lookaround makes the match the pronoun itself. The two `I` tokens collapse into one, since they differed only in the delimiter they required.  `nonword` goes too, which the PR was right about for a different reason: it prevents a project Vocab from applying to the rule.  No fixture covered this. Every `I` in the fixtures sits at the start of a line, where `^` matches zero-width and no space is consumed, so the existing expectations were identical either way. Added a mid-sentence case, which moves from column 10 with ' I' to column 11 with 'I'.") | 2 days agoJul 30, 2026 |
| [coverage](https://github.com/vale-cli/Microsoft/tree/master/coverage "coverage") | [coverage](https://github.com/vale-cli/Microsoft/tree/master/coverage "coverage") | [Update to Go tests and general refresh](https://github.com/vale-cli/Microsoft/commit/414362a553597e72fff7d7448404871bfd1c698f "Update to Go tests and general refresh") | 2 days agoJul 30, 2026 |
| [fixtures](https://github.com/vale-cli/Microsoft/tree/master/fixtures "fixtures") | [fixtures](https://github.com/vale-cli/Microsoft/tree/master/fixtures "fixtures") | [Narrow the FirstPerson match to the pronoun itself](https://github.com/vale-cli/Microsoft/commit/7a9a1217a2924a4d58bfdcbefae813ff9113b6b9 "Narrow the FirstPerson match to the pronoun itself  PR #72 reports bad underlines in editors using the language server and proposes removing `nonword: true`. The diagnosis is right, the change isn't sufficient: the token consumes the leading space, so mid-sentence \"Yesterday I walked\" matches \" I\" and the alert covers one character too many, reading \"such as ' I'\". Removing `nonword` leaves that unchanged.  Using lookaround makes the match the pronoun itself. The two `I` tokens collapse into one, since they differed only in the delimiter they required.  `nonword` goes too, which the PR was right about for a different reason: it prevents a project Vocab from applying to the rule.  No fixture covered this. Every `I` in the fixtures sits at the start of a line, where `^` matches zero-width and no space is consumed, so the existing expectations were identical either way. Added a mid-sentence case, which moves from column 10 with ' I' to column 11 with 'I'.") | 2 days agoJul 30, 2026 |
| [testdata](https://github.com/vale-cli/Microsoft/tree/master/testdata "testdata") | [testdata](https://github.com/vale-cli/Microsoft/tree/master/testdata "testdata") | [Narrow the FirstPerson match to the pronoun itself](https://github.com/vale-cli/Microsoft/commit/7a9a1217a2924a4d58bfdcbefae813ff9113b6b9 "Narrow the FirstPerson match to the pronoun itself  PR #72 reports bad underlines in editors using the language server and proposes removing `nonword: true`. The diagnosis is right, the change isn't sufficient: the token consumes the leading space, so mid-sentence \"Yesterday I walked\" matches \" I\" and the alert covers one character too many, reading \"such as ' I'\". Removing `nonword` leaves that unchanged.  Using lookaround makes the match the pronoun itself. The two `I` tokens collapse into one, since they differed only in the delimiter they required.  `nonword` goes too, which the PR was right about for a different reason: it prevents a project Vocab from applying to the rule.  No fixture covered this. Every `I` in the fixtures sits at the start of a line, where `^` matches zero-width and no space is consumed, so the existing expectations were identical either way. Added a mid-sentence case, which moves from column 10 with ' I' to column 11 with 'I'.") | 2 days agoJul 30, 2026 |
| [.gitignore](https://github.com/vale-cli/Microsoft/blob/master/.gitignore ".gitignore") | [.gitignore](https://github.com/vale-cli/Microsoft/blob/master/.gitignore ".gitignore") | [Update repo](https://github.com/vale-cli/Microsoft/commit/0aa3a8bac40aa81d02ff1e58f411dd01db7e66c4 "Update repo") | 3 years agoMay 11, 2023 |
| [.vale.ini](https://github.com/vale-cli/Microsoft/blob/master/.vale.ini ".vale.ini") | [.vale.ini](https://github.com/vale-cli/Microsoft/blob/master/.vale.ini ".vale.ini") | [Add .vale.ini](https://github.com/vale-cli/Microsoft/commit/37ec06b6dc66ad557d526769f90daf6bcd9d245a "Add .vale.ini") | 3 years agoMay 11, 2023 |
| [.yamllint.yml](https://github.com/vale-cli/Microsoft/blob/master/.yamllint.yml ".yamllint.yml") | [.yamllint.yml](https://github.com/vale-cli/Microsoft/blob/master/.yamllint.yml ".yamllint.yml") | [Remove 'document-start'](https://github.com/vale-cli/Microsoft/commit/eef21ef5cef08ea6dcaa1f2d0f82a82794f82e68 "Remove 'document-start'") | 8 years agoFeb 5, 2019 |
| [LICENSE](https://github.com/vale-cli/Microsoft/blob/master/LICENSE "LICENSE") | [LICENSE](https://github.com/vale-cli/Microsoft/blob/master/LICENSE "LICENSE") | [Update LICENSE](https://github.com/vale-cli/Microsoft/commit/ccedec01c32c5e40298b8fd4c75c58c8ac30a965 "Update LICENSE") | 8 years agoFeb 6, 2019 |
| [README.md](https://github.com/vale-cli/Microsoft/blob/master/README.md "README.md") | [README.md](https://github.com/vale-cli/Microsoft/blob/master/README.md "README.md") | [Update to Go tests and general refresh](https://github.com/vale-cli/Microsoft/commit/414362a553597e72fff7d7448404871bfd1c698f "Update to Go tests and general refresh") | 2 days agoJul 30, 2026 |
| [coverage\_test.go](https://github.com/vale-cli/Microsoft/blob/master/coverage_test.go "coverage_test.go") | [coverage\_test.go](https://github.com/vale-cli/Microsoft/blob/master/coverage_test.go "coverage_test.go") | [Update to Go tests and general refresh](https://github.com/vale-cli/Microsoft/commit/414362a553597e72fff7d7448404871bfd1c698f "Update to Go tests and general refresh") | 2 days agoJul 30, 2026 |
| [go.mod](https://github.com/vale-cli/Microsoft/blob/master/go.mod "go.mod") | [go.mod](https://github.com/vale-cli/Microsoft/blob/master/go.mod "go.mod") | [Update to Go tests and general refresh](https://github.com/vale-cli/Microsoft/commit/414362a553597e72fff7d7448404871bfd1c698f "Update to Go tests and general refresh") | 2 days agoJul 30, 2026 |
| [go.sum](https://github.com/vale-cli/Microsoft/blob/master/go.sum "go.sum") | [go.sum](https://github.com/vale-cli/Microsoft/blob/master/go.sum "go.sum") | [Update to Go tests and general refresh](https://github.com/vale-cli/Microsoft/commit/414362a553597e72fff7d7448404871bfd1c698f "Update to Go tests and general refresh") | 2 days agoJul 30, 2026 |
| [main.go](https://github.com/vale-cli/Microsoft/blob/master/main.go "main.go") | [main.go](https://github.com/vale-cli/Microsoft/blob/master/main.go "main.go") | [Update to Go tests and general refresh](https://github.com/vale-cli/Microsoft/commit/414362a553597e72fff7d7448404871bfd1c698f "Update to Go tests and general refresh") | 2 days agoJul 30, 2026 |
| [main\_test.go](https://github.com/vale-cli/Microsoft/blob/master/main_test.go "main_test.go") | [main\_test.go](https://github.com/vale-cli/Microsoft/blob/master/main_test.go "main_test.go") | [Update to Go tests and general refresh](https://github.com/vale-cli/Microsoft/commit/414362a553597e72fff7d7448404871bfd1c698f "Update to Go tests and general refresh") | 2 days agoJul 30, 2026 |
| View all files |

## Repository files navigation

# Microsoft

[Permalink: Microsoft](https://github.com/vale-cli/Microsoft#microsoft)

> **NOTE**: This project is neither maintained nor endorsed by Microsoft.

This repository contains a [Vale-compatible](https://github.com/errata-ai/vale) implementation of the [_Microsoft Writing Style Guide_](https://docs.microsoft.com/en-us/style-guide/welcome/) ( [LICENSE](https://github.com/MicrosoftDocs/microsoft-style-guide/blob/master/LICENSE)).

## Getting started

[Permalink: Getting started](https://github.com/vale-cli/Microsoft#getting-started)

To get started, add the package to your configuration file (as shown below) and then run `vale sync`.

```
StylesPath = styles
MinAlertLevel = suggestion

Packages = Microsoft

[*]
BasedOnStyles = Vale, Microsoft
```

See [Packages](https://vale.sh/hub/microsoft/) for more information.

## Repository structure

[Permalink: Repository structure](https://github.com/vale-cli/Microsoft#repository-structure)

[`/Microsoft`](https://github.com/errata-ai/Microsoft/tree/master/Microsoft)The [YAML](http://yaml.org/)-based rule implementations that make up our style.[`/fixtures`](https://github.com/errata-ai/Microsoft/tree/master/fixtures)The individual unit tests. Each directory should be named after a rule found in `/Microsoft` and include its own `.vale.ini` file that isolates its target rule.[`/testdata`](https://github.com/errata-ai/Microsoft/tree/master/testdata)The expected Vale output for each fixture directory, one `<Rule>.ct` file per fixture. We use [go-cmdtest](https://github.com/google/go-cmdtest) to run Vale against each fixture and compare its output. Run the suite with `go test ./...`; regenerate the expectations after an intentional change with `go test ./... -update`.[`/coverage`](https://github.com/errata-ai/Microsoft/tree/master/coverage)How much of the style guide we implement, tracked topic by topic. Each file mirrors one top-level section of the guide, and each key is a subtopic set to `true` or `false`, optionally followed by a comment naming the rules that implement it.

## Coverage

[Permalink: Coverage](https://github.com/vale-cli/Microsoft#coverage)

Run `go test -v -run TestCoverage ./...` to print the current figures:

```
  guidelines:     37/64 (57.8%)
  A-Z word list:  106/849 (12.5%)
```

The two are reported separately because the A–Z word list is roughly ten times
the size of everything else, so a single combined percentage tells you almost
nothing about the guidelines.

The same test enforces what keeps the number honest: values must be exactly
`true` or `false`, and every rule named in a comment must still exist. A rule
that's renamed or merged away therefore can't leave a topic silently claiming
coverage it no longer has.

Sections of the guide that describe process rather than prose have no manifest,
since there's nothing there for a linter to check: Checklists, Content planning,
Design planning, Final publishing review, Search and writing, and Top 10 tips.
Scannable content and Text formatting are also absent for now; their
lintable subtopics (headings, sentence-style capitalization) are already counted
under `capitalization.yml`, and listing them again would double-count.

## Extension points

[Permalink: Extension points](https://github.com/vale-cli/Microsoft#extension-points)

| Check | Implementations |
| :-: | :-- |

[... middle omitted — see footer ...]

| [`substitution`](https://vale.sh/docs/checks/substitution) | [`BiasFree.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/BiasFree.yml), [`Contractions.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/Contractions.yml), [`Foreign.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/Foreign.yml), [`GenderBias.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/GenderBias.yml), [`Jargon.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/Jargon.yml), [`Militaristic.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/Militaristic.yml), [`Terms.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/Terms.yml), [`URLFormat.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/URLFormat.yml), [`Wordiness.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/Wordiness.yml) |
| [`occurrence`](https://vale.sh/docs/checks/occurrence) | [`SentenceLength.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/SentenceLength.yml) |
| [`repetition`](https://vale.sh/docs/checks/repetition) | N/A |
| [`consistency`](https://vale.sh/docs/checks/consistency) | N/A |
| [`capitalization`](https://vale.sh/docs/checks/capitalization) | [`Headings.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/Headings.yml) |
| [`conditional`](https://vale.sh/docs/checks/conditional) | [`Acronyms.yml`](https://github.com/errata-ai/Microsoft/blob/master/Microsoft/Acronyms.yml) |
| [`metric`](https://vale.sh/docs/checks/metric) | N/A |
| [`spelling`](https://vale.sh/docs/checks/spelling) | N/A |
| [`sequence`](https://vale.sh/docs/checks/sequence) | N/A |
| [`script`](https://vale.sh/docs/checks/script) | N/A |
| [`readability`](https://vale.sh/docs/checks/readability) | N/A |

## About

A Vale-compatible implementation of the Microsoft Writing Style Guide.

[github.com/errata-ai/vale](https://github.com/errata-ai/vale)

### Topics

[vale](https://github.com/topics/vale) [vale-linter-style](https://github.com/topics/vale-linter-style) [vale-style](https://github.com/topics/vale-style)

### Resources

[Readme](https://github.com/vale-cli/Microsoft#readme-ov-file)

[MIT license](https://github.com/vale-cli/Microsoft#MIT-1-ov-file)

[Activity](https://github.com/vale-cli/Microsoft/activity)

[Custom properties](https://github.com/vale-cli/Microsoft/custom-properties)

### Stars

[**110** stars](https://github.com/vale-cli/Microsoft/stargazers)

### Watchers

[**13** watching](https://github.com/vale-cli/Microsoft/watchers)

### Forks

[**55** forks](https://github.com/vale-cli/Microsoft/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fvale-cli%2FMicrosoft&report=vale-cli+%28user%29)

## Releases

## Sponsor this project

## Packages

## Used by

## Contributors

## Languages

You can’t perform that action at this time.

──────── [TRUNCATED] ────────
Showing 14,761 chars (head) + 2,948 chars (tail) of 21,075 total clean characters.
Full text saved to: /Users/nikola/.hermes/profiles/ste-code/cache/web/github.com-6bb413bcae.md
To read the omitted middle: read_file path="/Users/nikola/.hermes/profiles/ste-code/cache/web/github.com-6bb413bcae.md" offset=212 limit=200  (the file is the complete page; raise/lower offset to page through it).
─────────────────────────────