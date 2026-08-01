# errata-ai/Google

> Source: https://github.com/errata-ai/Google
> Fetched by finalize reference fetcher.

---

[Skip to content](https://github.com/vale-cli/Google#start-of-content)

You signed in with another tab or window. [Reload](https://github.com/vale-cli/Google) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/vale-cli/Google) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/vale-cli/Google) to refresh your session.Dismiss alert

{{ message }}

### Uh oh!

There was an error while loading. [Please reload this page](https://github.com/vale-cli/Google).

[vale-cli](https://github.com/vale-cli)/ **[Google](https://github.com/vale-cli/Google)** Public

- ### Uh oh!







There was an error while loading. [Please reload this page](https://github.com/vale-cli/Google).

- [Notifications](https://github.com/login?return_to=%2Fvale-cli%2FGoogle) You must be signed in to change notification settings
- [Fork\\
26](https://github.com/login?return_to=%2Fvale-cli%2FGoogle)
- [Star\\
87](https://github.com/login?return_to=%2Fvale-cli%2FGoogle)


master

[**1** Branch](https://github.com/vale-cli/Google/branches) [**17** Tags](https://github.com/vale-cli/Google/tags)

[Go to Branches page](https://github.com/vale-cli/Google/branches)[Go to Tags page](https://github.com/vale-cli/Google/tags)

Go to file

Code

Open more actions menu

## Folders and files

| Name | Name | Last commit message | Last commit date |
| --- | --- | --- | --- |
| ## Latest commit<br>## History<br>[92 Commits](https://github.com/vale-cli/Google/commits/master/) <br>[View commit history for this file.](https://github.com/vale-cli/Google/commits/master/) 92 Commits |
| [.github/workflows](https://github.com/vale-cli/Google/tree/master/.github/workflows "This path skips through empty directories") | [.github/workflows](https://github.com/vale-cli/Google/tree/master/.github/workflows "This path skips through empty directories") |  |  |
| [Google](https://github.com/vale-cli/Google/tree/master/Google "Google") | [Google](https://github.com/vale-cli/Google/tree/master/Google "Google") |  |  |
| [coverage](https://github.com/vale-cli/Google/tree/master/coverage "coverage") | [coverage](https://github.com/vale-cli/Google/tree/master/coverage "coverage") |  |  |
| [fixtures](https://github.com/vale-cli/Google/tree/master/fixtures "fixtures") | [fixtures](https://github.com/vale-cli/Google/tree/master/fixtures "fixtures") |  |  |
| [testdata](https://github.com/vale-cli/Google/tree/master/testdata "testdata") | [testdata](https://github.com/vale-cli/Google/tree/master/testdata "testdata") |  |  |
| [.gitignore](https://github.com/vale-cli/Google/blob/master/.gitignore ".gitignore") | [.gitignore](https://github.com/vale-cli/Google/blob/master/.gitignore ".gitignore") |  |  |
| [.vale.ini](https://github.com/vale-cli/Google/blob/master/.vale.ini ".vale.ini") | [.vale.ini](https://github.com/vale-cli/Google/blob/master/.vale.ini ".vale.ini") |  |  |
| [.yamllint.yml](https://github.com/vale-cli/Google/blob/master/.yamllint.yml ".yamllint.yml") | [.yamllint.yml](https://github.com/vale-cli/Google/blob/master/.yamllint.yml ".yamllint.yml") |  |  |
| [LICENSE](https://github.com/vale-cli/Google/blob/master/LICENSE "LICENSE") | [LICENSE](https://github.com/vale-cli/Google/blob/master/LICENSE "LICENSE") |  |  |
| [README.md](https://github.com/vale-cli/Google/blob/master/README.md "README.md") | [README.md](https://github.com/vale-cli/Google/blob/master/README.md "README.md") |  |  |
| [coverage\_test.go](https://github.com/vale-cli/Google/blob/master/coverage_test.go "coverage_test.go") | [coverage\_test.go](https://github.com/vale-cli/Google/blob/master/coverage_test.go "coverage_test.go") |  |  |
| [go.mod](https://github.com/vale-cli/Google/blob/master/go.mod "go.mod") | [go.mod](https://github.com/vale-cli/Google/blob/master/go.mod "go.mod") |  |  |
| [go.sum](https://github.com/vale-cli/Google/blob/master/go.sum "go.sum") | [go.sum](https://github.com/vale-cli/Google/blob/master/go.sum "go.sum") |  |  |
| [main.go](https://github.com/vale-cli/Google/blob/master/main.go "main.go") | [main.go](https://github.com/vale-cli/Google/blob/master/main.go "main.go") |  |  |
| [main\_test.go](https://github.com/vale-cli/Google/blob/master/main_test.go "main_test.go") | [main\_test.go](https://github.com/vale-cli/Google/blob/master/main_test.go "main_test.go") |  |  |
| View all files |

## Repository files navigation

# Google

[Permalink: Google](https://github.com/vale-cli/Google#google)

> **NOTE**: This project is neither maintained nor endorsed by Google.

This repository contains a [Vale-compatible](https://github.com/errata-ai/vale) implementation of the [_Google Developer Documentation Style Guide_](https://developers.google.com/style/) ( [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).

## Getting Started

[Permalink: Getting Started](https://github.com/vale-cli/Google#getting-started)

To get started, add the package to your configuration file (as shown below) and then run `vale sync`.

```
StylesPath = styles
MinAlertLevel = suggestion

Packages = Google

[*]
BasedOnStyles = Vale, Google
```

See [Packages](https://vale.sh/docs/keys/packages) for more information.

## Repository Structure

[Permalink: Repository Structure](https://github.com/vale-cli/Google#repository-structure)

[`/Google`](https://github.com/errata-ai/Google/tree/master/Google)The [YAML](http://yaml.org/)-based rule implementations that make up our style.[`/fixtures`](https://github.com/errata-ai/Google/tree/master/fixtures)The individual unit tests. Each directory should be named after a rule found in `/Google` and include its own `.vale.ini` file that isolates its target rule.[`/testdata`](https://github.com/errata-ai/Google/tree/master/testdata)The expected Vale output for each fixture directory, one `<Rule>.ct` file per fixture. We use [go-cmdtest](https://github.com/google/go-cmdtest) to run Vale against each fixture and compare its output. Run the suite with `go test ./...`; regenerate the expectations after an intentional change with `go test ./... -update`.[`/coverage`](https://github.com/errata-ai/Google/tree/master/coverage)How much of the style guide we implement, tracked topic by topic. Each key is a subtopic set to `true` or `false`, optionally followed by a comment naming the rules that implement it. Run `go test -v -run TestCoverage ./...` to print the current figures; the same test fails if a named rule no longer exists, so a topic can't silently claim coverage it has lost.

## About

A Vale-compatible implementation of the Google Developer Documentation Style Guide.

### Topics

[vale](https://github.com/topics/vale) [vale-linter-style](https://github.com/topics/vale-linter-style) [vale-style](https://github.com/topics/vale-style)

### Resources

[Readme](https://github.com/vale-cli/Google#readme-ov-file)

[MIT license](https://github.com/vale-cli/Google#MIT-1-ov-file)

[Activity](https://github.com/vale-cli/Google/activity)

[Custom properties](https://github.com/vale-cli/Google/custom-properties)

### Stars

[**87** stars](https://github.com/vale-cli/Google/stargazers)

### Watchers

[**4** watching](https://github.com/vale-cli/Google/watchers)

### Forks

[**26** forks](https://github.com/vale-cli/Google/forks)

[Report repository](https://github.com/contact/report-content?content_url=https%3A%2F%2Fgithub.com%2Fvale-cli%2FGoogle&report=vale-cli+%28user%29)

## Releases

## Sponsor this project

## Packages

## Used by

## Contributors

## Languages

You can’t perform that action at this time.