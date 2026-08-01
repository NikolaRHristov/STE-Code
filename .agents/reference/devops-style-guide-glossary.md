# DevOps Style Guide Glossary

> Source: https://tydukes.github.io/coding-style-guide/glossary/
> Fetched by finalize reference fetcher.

---

[Skip to content](https://tydukes.github.io/coding-style-guide/glossary/#a)

[Edit this page](https://github.com/tydukes/coding-style-guide/edit/main/docs/glossary.md "Edit this page")

# Glossary

This glossary defines terms used throughout the DevOps Engineering Style Guide, including technical concepts, tool names,
metadata tags, and industry terminology.

Quick Navigation

Use your browser's search (Ctrl+F / Cmd+F) or the site search bar to find
specific terms. See also the [Topic Index](https://tydukes.github.io/coding-style-guide/topic_index/) for browsing by
subject area and the [FAQ](https://tydukes.github.io/coding-style-guide/faq/) for common questions.

## A [¶](https://tydukes.github.io/coding-style-guide/glossary/\#a "Permanent link")

### AI Assistant [¶](https://tydukes.github.io/coding-style-guide/glossary/\#ai-assistant "Permanent link")

A software tool that uses artificial intelligence to help with code writing, review, and understanding. Examples include
Claude, GitHub Copilot, and ChatGPT. The style guide optimizes code metadata for better AI comprehension.

### Ansible [¶](https://tydukes.github.io/coding-style-guide/glossary/\#ansible "Permanent link")

An open-source automation tool for configuration management, application deployment, and task automation. Uses YAML
playbooks to define infrastructure as code. See the [Ansible Style Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/ansible/).

### ArgoCD [¶](https://tydukes.github.io/coding-style-guide/glossary/\#argocd "Permanent link")

A declarative GitOps continuous delivery tool for Kubernetes. Monitors Git repositories and automatically syncs
application state to match declared configuration. See [GitOps Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/gitops/).

### API (Application Programming Interface) [¶](https://tydukes.github.io/coding-style-guide/glossary/\#api-application-programming-interface "Permanent link")

A set of rules and protocols that allows different software applications to communicate with each other. Commonly refers
to RESTful HTTP APIs in web services.

### API Endpoint [¶](https://tydukes.github.io/coding-style-guide/glossary/\#api-endpoint "Permanent link")

A specific URL path and HTTP method combination that provides access to a resource or function in an API. Example:
`POST /auth/login`.

### Automation [¶](https://tydukes.github.io/coding-style-guide/glossary/\#automation "Permanent link")

The use of tools and scripts to perform tasks automatically without manual intervention. Core principle of the style
guide for enforcing standards.

## B [¶](https://tydukes.github.io/coding-style-guide/glossary/\#b "Permanent link")

### AWS CDK (Cloud Development Kit) [¶](https://tydukes.github.io/coding-style-guide/glossary/\#aws-cdk-cloud-development-kit "Permanent link")

A framework for defining cloud infrastructure using familiar programming languages (TypeScript, Python, Go, Java)
instead of YAML/JSON templates. See the [AWS CDK Style Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/cdk/).

### Bash [¶](https://tydukes.github.io/coding-style-guide/glossary/\#bash "Permanent link")

Unix shell and command language used for scripting and automation. Commonly used for deployment scripts, CI/CD
pipelines, and system administration tasks. See the [Bash Style Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/bash/).

### Bicep [¶](https://tydukes.github.io/coding-style-guide/glossary/\#bicep "Permanent link")

A domain-specific language for deploying Azure resources declaratively. Compiles to ARM templates with cleaner syntax.
See the [Bicep Style Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/bicep/).

### Black [¶](https://tydukes.github.io/coding-style-guide/glossary/\#black "Permanent link")

An opinionated Python code formatter that automatically formats code to a consistent style. Eliminates debates about
formatting by providing one standard style.

### Block Comment [¶](https://tydukes.github.io/coding-style-guide/glossary/\#block-comment "Permanent link")

A multi-line comment enclosed in special syntax. Example in Terraform: `/* comment */`, in Python:
`"""docstring"""`.

### Boolean [¶](https://tydukes.github.io/coding-style-guide/glossary/\#boolean "Permanent link")

A data type with two possible values: `true` or `false`. Often used for configuration flags and conditional logic.

### Branch [¶](https://tydukes.github.io/coding-style-guide/glossary/\#branch "Permanent link")

A parallel version of a repository in version control. Allows development of features in isolation from the main
codebase.

### Breaking Change [¶](https://tydukes.github.io/coding-style-guide/glossary/\#breaking-change "Permanent link")

A modification to code or API that is not backward-compatible and requires users to update their code. Triggers a
MAJOR version increment in semantic versioning.

## C [¶](https://tydukes.github.io/coding-style-guide/glossary/\#c "Permanent link")

### camelCase [¶](https://tydukes.github.io/coding-style-guide/glossary/\#camelcase "Permanent link")

A naming convention where the first word is lowercase and subsequent words are capitalized. Example:
`getUserDetails`. Common in JavaScript and TypeScript.

### Chaos Engineering [¶](https://tydukes.github.io/coding-style-guide/glossary/\#chaos-engineering "Permanent link")

The practice of intentionally introducing failures into a system to test its resilience and identify weaknesses before
they cause real outages. See the [Chaos Engineering Guide](https://tydukes.github.io/coding-style-guide/05_ci_cd/chaos_engineering_guide/).

### CI/CD (Continuous Integration / Continuous Deployment) [¶](https://tydukes.github.io/coding-style-guide/glossary/\#cicd-continuous-integration-continuous-deployment "Permanent link")

Practices that automate the building, testing, and deployment of code. CI runs automated tests on every commit; CD
automatically deploys passing code to production. See [CI/CD guides](https://tydukes.github.io/coding-style-guide/05_ci_cd/github_actions_guide/).

### CloudFormation [¶](https://tydukes.github.io/coding-style-guide/glossary/\#cloudformation "Permanent link")

AWS service for provisioning infrastructure using JSON or YAML templates. Manages resources as stacks with
rollback support. See the [CloudFormation Style Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/cloudformation/).

### Code-to-Text Ratio [¶](https://tydukes.github.io/coding-style-guide/glossary/\#code-to-text-ratio "Permanent link")

A quality metric specific to this style guide requiring at least 3 lines of code examples for every 1 line of
explanatory text in language guides. Enforces "show, don't tell" documentation philosophy.

### Conventional Commits [¶](https://tydukes.github.io/coding-style-guide/glossary/\#conventional-commits "Permanent link")

A specification for adding human and machine-readable meaning to commit messages. Format: `type(scope): subject`.
Required for all commits in this project. Types include: feat, fix, docs, style, refactor, test, chore.

### Crossplane [¶](https://tydukes.github.io/coding-style-guide/glossary/\#crossplane "Permanent link")

A Kubernetes-native infrastructure as code tool that enables provisioning cloud resources using Kubernetes-style
manifests. See the [Crossplane Style Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/crossplane/).

### cSpell [¶](https://tydukes.github.io/coding-style-guide/glossary/\#cspell "Permanent link")

A spell checker for code and documentation. Used in CI to block merges with spelling errors. Custom dictionary at
`.github/cspell.json`.

### CLI (Command-Line Interface) [¶](https://tydukes.github.io/coding-style-guide/glossary/\#cli-command-line-interface "Permanent link")

A text-based interface for interacting with software through commands typed into a terminal. Example: `git commit -m
"message"`.

### Code Review [¶](https://tydukes.github.io/coding-style-guide/glossary/\#code-review "Permanent link")

The process of examining code changes before they are merged, typically through pull requests. Focuses on logic,
architecture, and design rather than formatting.

### Container [¶](https://tydukes.github.io/coding-style-guide/glossary/\#container "Permanent link")

A lightweight, standalone package of software that includes everything needed to run an application: code, runtime,
libraries, and dependencies. Docker is the most common container platform.

### Convention [¶](https://tydukes.github.io/coding-style-guide/glossary/\#convention "Permanent link")

An agreed-upon standard or pattern used consistently across a codebase. Examples include naming conventions and
code structure patterns.

## D [¶](https://tydukes.github.io/coding-style-guide/glossary/\#d "Permanent link")

### DAST (Dynamic Application Security Testing) [¶](https://tydukes.github.io/coding-style-guide/glossary/\#dast-dynamic-application-security-testing "Permanent link")

Security testing that analyzes a running application for vulnerabilities. Contrast with SAST which analyzes source
code. See [Security Scanning Guide](https://tydukes.github.io/coding-style-guide/05_ci_cd/security_scanning_guide/).

### Dependency [¶](https://tydukes.github.io/coding-style-guide/glossary/\#dependency "Permanent link")

An external library, package, or module that code relies on to function. Should be documented in metadata tags.
See [Dependency Update Policies](https://tydukes.github.io/coding-style-guide/05_ci_cd/dependency_update_policies/).

### Dependabot [¶](https://tydukes.github.io/coding-style-guide/glossary/\#dependabot "Permanent link")

A GitHub tool that automatically creates pull requests to update outdated dependencies. See
[Dependabot Auto-Merge](https://tydukes.github.io/coding-style-guide/05_ci_cd/dependabot_auto_merge/).

### Dev Container [¶](https://tydukes.github.io/coding-style-guide/glossary/\#dev-container "Permanent link")

A Docker-based development environment defined by a `devcontainer.json` file. Ensures consistent tooling across team
members. See the [Dev Container Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/devcontainer/).

### Deployment [¶](https://tydukes.github.io/coding-style-guide/glossary/\#deployment "Permanent link")

The process of releasing software to a target environment (production, staging, or development).

### Deprecation [¶](https://tydukes.github.io/coding-style-guide/glossary/\#deprecation "Permanent link")

Marking a feature, function, or module as obsolete and scheduled for removal. Uses `@status deprecated` metadata
tag.

### Development Environment [¶](https://tydukes.github.io/coding-style-guide/glossary/\#development-environment "Permanent link")

The local or remote system where developers write and test code, typically with debugging tools and test data.

### DevOps [¶](https://tydukes.github.io/coding-style-guide/glossary/\#devops "Permanent link")

A set of practices that combines software development (Dev) and IT operations (Ops) to shorten development cycles and
deliver high-quality software.

### Docker [¶](https://tydukes.github.io/coding-style-guide/glossary/\#docker "Permanent link")

A platform for developing, shipping, and running applications in containers. Ensures consistency across development,
testing, and production environments. See [Dockerfile Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/dockerfile/) and
[Docker Compose Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/docker_compose/).

### Documentation [¶](https://tydukes.github.io/coding-style-guide/glossary/\#documentation "Permanent link")

Written explanations of how code works, including inline comments, README files, and generated API docs.
Auto-generated from metadata in this style guide.

### Dry Run [¶](https://tydukes.github.io/coding-style-guide/glossary/\#dry-run "Permanent link")

Executing a command in simulation mode without making actual changes. Useful for testing potentially destructive
operations.

## E [¶](https://tydukes.github.io/coding-style-guide/glossary/\#e "Permanent link")

### EditorConfig [¶](https://tydukes.github.io/coding-style-guide/glossary/\#editorconfig "Permanent link")

A file format and collection of editor plugins for maintaining consistent coding styles across different editors and
IDEs.

### Environment Variable [¶](https://tydukes.github.io/coding-style-guide/glossary/\#environment-variable "Permanent link")

A dynamic value that can affect how processes behave on a computer. Often used to configure applications without
hardcoding values. Example: `API_KEY=abc123`.

### EOF (End of File) [¶](https://tydukes.github.io/coding-style-guide/glossary/\#eof-end-of-file "Permanent link")

A marker indicating the end of a file. Files should end with exactly one blank line per style guide convention.

### ESLint [¶](https://tydukes.github.io/coding-style-guide/glossary/\#eslint "Permanent link")

A static analysis tool for identifying problematic patterns in JavaScript/TypeScript code. Enforces code quality and
style rules.

### Flux [¶](https://tydukes.github.io/coding-style-guide/glossary/\#flux "Permanent link")

A GitOps tool for keeping Kubernetes clusters in sync with configuration sources (Git repositories). Alternative to
ArgoCD. See [GitOps Guide](https://tydukes.github.io/coding-style-guide/02_language_guides/gitops/).

## F [¶](https://tydukes.github.io/coding-style-guide/glossary/\#f "Permanent link")

### Feature Branch [¶](https://tydukes.github.io/coding-style-guide/glossary/\#feature-branch "Permanent link")

A git branch created to develop a specific feature in isolation. Named with `feature/` prefix. Example:
`feature/add-user-auth`.

### Flake8 [¶](https://tydukes.github.io/coding-style-guide/glossary/\#flake8 "Permanent link")

A Python linting tool that checks code for style violations, programming errors, and complexity. Combines pycodestyle,
pyflakes, and McCabe.

### Formatter [¶](https://tydukes.github.io/coding-style-guide/glossary/\#formatter "Permanent link")

A tool that automatically reformats code to match style guidelines. Examples include Black (Python), Prettier
(JavaScript/TypeScript), and terraform fmt.

### Function [¶](https://tydukes.github.io/coding-style-guide/glossary/\#function "Permanent link")

A reusable block of code that performs a specific task. Should be named with verb-noun format: `get_user()`,
`calculate_total()`.

## G [¶](https://tydukes.github.io/coding-style-guide/glossary/\#g "Permanent link")

### Git [¶](https://tydukes.github.io/coding-style-guide/glossary/\#git "Permanent link")

A distributed version control system for tracking changes in source code during software development.


[... middle omitted — see footer ...]

| File name | `snake_case.py` | `kebab-case.ts` | `snake_case.go` | `snake_case.tf` | `kebab-case.sh` |
| Module/Package | `snake_case` | `kebab-case` | `lowercase` | `snake_case` | N/A |
| Boolean | `is_active` | `isActive` | `isActive` | `enable_feature` | N/A |

See the [Language Comparison Matrix](https://tydukes.github.io/coding-style-guide/02_language_guides/comparison_matrix/) for a complete feature comparison.

* * *

## Common Abbreviations [¶](https://tydukes.github.io/coding-style-guide/glossary/\#common-abbreviations "Permanent link")

- **API**: Application Programming Interface
- **AWS**: Amazon Web Services
- **CI**: Continuous Integration
- **CD**: Continuous Deployment/Delivery
- **CDK**: Cloud Development Kit
- **CLI**: Command-Line Interface
- **DAST**: Dynamic Application Security Testing
- **DRY**: Don't Repeat Yourself
- **EOF**: End of File
- **HCL**: HashiCorp Configuration Language
- **HTTP**: Hypertext Transfer Protocol
- **IAC**: Infrastructure as Code
- **IDE**: Integrated Development Environment
- **JSON**: JavaScript Object Notation
- **JWT**: JSON Web Token
- **K8s**: Kubernetes (8 characters between K and s)
- **LSP**: Language Server Protocol
- **NAT**: Network Address Translation
- **OAuth**: Open Authorization
- **OOP**: Object-Oriented Programming
- **OPA**: Open Policy Agent
- **OS**: Operating System
- **PR**: Pull Request
- **REST**: Representational State Transfer
- **SAST**: Static Application Security Testing
- **SBOM**: Software Bill of Materials
- **SEMVER**: Semantic Versioning
- **SRE**: Site Reliability Engineering
- **SQL**: Structured Query Language
- **SSH**: Secure Shell
- **SSL**: Secure Sockets Layer
- **TLS**: Transport Layer Security
- **URL**: Uniform Resource Locator
- **UUID**: Universally Unique Identifier
- **VCS**: Version Control System
- **VPC**: Virtual Private Cloud
- **TOML**: Tom's Obvious, Minimal Language
- **XRD**: Composite Resource Definition (Crossplane)
- **YAML**: YAML Ain't Markup Language

* * *

## Tool Names Quick Reference [¶](https://tydukes.github.io/coding-style-guide/glossary/\#tool-names-quick-reference "Permanent link")

### Formatters [¶](https://tydukes.github.io/coding-style-guide/glossary/\#formatters "Permanent link")

- **Black**: Python code formatter
- **Prettier**: Multi-language code formatter (JS/TS/JSON/YAML)
- **terraform fmt**: Terraform configuration formatter
- **shfmt**: Shell script formatter

### Linters [¶](https://tydukes.github.io/coding-style-guide/glossary/\#linters "Permanent link")

- **Flake8**: Python linter (style + errors)
- **Pylint**: Comprehensive Python linter
- **ESLint**: JavaScript/TypeScript linter
- **ShellCheck**: Bash/shell script linter
- **tflint**: Terraform linter
- **yamllint**: YAML linter
- **markdownlint**: Markdown linter

### Type Checkers [¶](https://tydukes.github.io/coding-style-guide/glossary/\#type-checkers "Permanent link")

- **mypy**: Python static type checker
- **tsc**: TypeScript compiler and type checker

### Testing Frameworks [¶](https://tydukes.github.io/coding-style-guide/glossary/\#testing-frameworks "Permanent link")

- **pytest**: Python testing framework
- **Jest**: JavaScript/TypeScript testing framework
- **Mocha**: JavaScript test framework
- **RSpec**: Ruby testing framework

### Build Tools [¶](https://tydukes.github.io/coding-style-guide/glossary/\#build-tools "Permanent link")

- **Make**: Build automation tool
- **Gradle**: Build automation for Java/Kotlin
- **Maven**: Build automation and dependency management for Java
- **npm**: Node.js package manager and build tool
- **uv**: Fast Python package installer

### CI/CD Platforms [¶](https://tydukes.github.io/coding-style-guide/glossary/\#cicd-platforms "Permanent link")

- **GitHub Actions**: CI/CD integrated with GitHub
- **GitLab CI**: CI/CD integrated with GitLab
- **Jenkins**: Open-source automation server
- **CircleCI**: Cloud-based CI/CD platform
- **Travis CI**: CI service for GitHub projects

### IaC Testing Tools [¶](https://tydukes.github.io/coding-style-guide/glossary/\#iac-testing-tools "Permanent link")

- **Terratest**: Go-based testing framework for Terraform
- **Kitchen-Terraform**: Test Kitchen plugin for Terraform
- **InSpec**: Compliance automation framework
- **OPA/Conftest**: Policy testing for structured data
- **Checkov**: Static analysis for IaC security

### Security Scanning Tools [¶](https://tydukes.github.io/coding-style-guide/glossary/\#security-scanning-tools "Permanent link")

- **Trivy**: Container and IaC vulnerability scanner
- **Snyk**: Developer security platform
- **Bandit**: Python security linter
- **Semgrep**: Lightweight static analysis for many languages
- **OWASP ZAP**: Dynamic application security testing

* * *

**Total Terms**: 200+

For additional terms or clarifications, please refer to the specific language guides or open an issue on the
[GitHub repository](https://github.com/tydukes/coding-style-guide/issues).

Back to top

──────── [TRUNCATED] ────────
Showing 14,888 chars (head) + 4,976 chars (tail) of 52,810 total clean characters.
Full text saved to: /Users/nikola/.hermes/profiles/ste-code/cache/web/tydukes.github.io-d461b91219.md
To read the omitted middle: read_file path="/Users/nikola/.hermes/profiles/ste-code/cache/web/tydukes.github.io-d461b91219.md" offset=261 limit=200  (the file is the complete page; raise/lower offset to page through it).
─────────────────────────────