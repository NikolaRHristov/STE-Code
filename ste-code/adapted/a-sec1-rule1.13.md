# Rule 1.13 — Do Not Use Technical Verbs as Nouns

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.13

## Original Rule

**Rule 1.13** Do not use technical verbs as nouns.

In English, words that look the same do not always have the same function in a sentence. Use technical verbs only as verbs, not as nouns.

Example:

> **STE:** Enter your password.

("Enter" is a technical verb, category 2 a), computer processes and applications, input and output processes.)

Words that can be technical verbs and technical nouns

In some contexts, the same word can be a technical verb and a technical noun. This condition occurs when you can put this word in a technical verb category (rule 1.12) and in a technical noun category (rule 1.5).

> **STE:** There are two methods to plate the ring nut (2).

("Plate" is a technical verb, category 1 c), manufacturing processes, attach material.)

## STE-Code Adaptation

**Rule 1.13** Do not use code-domain technical verbs as nouns.

> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs

In English, words that look the same do not always have the same function in a sentence. Use code-domain technical verbs only as verbs, not as nouns. If you need to use a word as a noun, find an approved noun or a code-domain technical noun that has the equivalent meaning.

This adapts the spec principle: just as you cannot use "enter" as a noun in STE (you must use it only as a verb, as in "Enter your password"), you cannot use code-domain technical verbs as nouns in STE-Code.

In some contexts, the same word can be a code-domain technical verb and a code-domain technical noun. This condition occurs when you can put this word in a code-domain technical verb category (rule 1.12) and in a code-domain technical noun category (rule 1.5). This adapts the spec example where "plate" can be a technical verb (a manufacturing process) — the spec explicitly acknowledges that some words can belong to both category systems.

### Code-Domain Explanation

This rule applies across all forms of code documentation. Each documentation type has different risk patterns for verb-as-noun misuse.

**README files** — README files frequently describe project workflows in noun-heavy prose. A common error is nominalizing build and deployment verbs: "Do a build of the project" instead of "Build the project." README files must use imperative verb forms for setup instructions.

**API documentation** — API reference docs describe operations that return results. Do not nominalize the operation: "The function does a parse of the input string" must become "The function parses the input string." However, when the API returns a named artifact (for example, a `Build` object, a `Deployment` resource), the noun form is a technical noun (rule 1.5), not a misused verb.

**Docstrings and inline comments** — Docstrings describe what a function or method does. Use the verb form: "Compiles the source files" not "Does a compile of the source files." Comments that explain why a line exists must use verb forms for actions: "// Retry the connection" not "// A retry of the connection."

**Commit messages** — Commit messages describe what the commit does. The conventional commit format uses the imperative: "Add login endpoint" not "Addition of login endpoint." The commit subject line is a command — it tells the codebase what to do. Using a verb as a noun in a commit message hides the action.

**Error messages** — Error messages must describe what failed and what to do. Use verb forms: "Failed to compile module 'auth'" not "Compile of module 'auth' failed." The reader needs to know the action that did not complete.

**Log output** — Log lines describe events. Use verb forms for actions: "Deploy started for release v2.1.0" not "Start of deploy for release v2.1.0." Log aggregation tools parse action verbs more reliably than nominalized forms.

### Paradigm-Specific Guidance

The verb-as-noun risk varies by programming paradigm because each paradigm has a different set of common technical verbs.

**Object-Oriented (Java, C++, C#, Python classes)**

OOP documentation frequently nominalizes instantiation and lifecycle verbs. Common violations:

- "Create an instantiate of the class" → "Instantiate the class"
- "Do an initialize of the service" → "Initialize the service"
- "Call the dispose method" → "The dispose method" can be correct if "dispose" is a method name (technical noun, rule 1.5). The instruction must say "Call the dispose method," not "Do a dispose."

OOP design patterns use noun-heavy language naturally (Factory, Builder, Observer). These pattern names are code-domain technical nouns (rule 1.5), not verbs used as nouns. Distinguish carefully: "Use the Builder to construct the object" (Builder = technical noun, construct = approved verb) versus "Do a build of the object" (build = misused verb).

**Functional (Haskell, Elixir, Clojure, Rust)**

Functional programming documentation often nominalizes transformation verbs. Common violations:

- "Do a map over the list" → "Map over the list" or "Apply the map function to the list"
- "Do a filter of the collection" → "Filter the collection"
- "Do a reduce on the array" → "Reduce the array"

When a function name is also a verb (map, filter, reduce, fold, compose, curry), use the word as a verb in instructions and as a function name (technical noun) in type signatures. In type signatures, "map" is a function reference (technical noun, rule 1.5). In instructions, "map" is a verb (technical verb, rule 1.12).

**Procedural (C, Go, Bash)**

Procedural code documentation frequently nominalizes memory and I/O verbs. Common violations:

- "Do an allocate of memory" → "Allocate memory"
- "Do a read from the file descriptor" → "Read from the file descriptor"
- "Do a write to the buffer" → "Write to the buffer"
- "Make a copy of the struct" → "Copy the struct"

C and Go use short, action-oriented function names (malloc, read, write, copy, send, recv). In documentation, use these as verbs: "malloc allocates memory on the heap" not "malloc does an allocation."

**Declarative (SQL, Terraform, Kubernetes YAML)**

Declarative documentation describes desired state. The configuration file declares what must exist, but the documentation that explains how to write the configuration uses imperative verbs. Common violations:

- "Do an apply of the manifest" → "Apply the manifest"
- "Do a plan of the infrastructure" → "Plan the infrastructure" or "Run `terraform plan`"
- "Do a select from the table" → "Select from the table" or "Run a SELECT query"

In SQL documentation, SELECT, INSERT, UPDATE, and DELETE are keyword names (technical nouns, rule 1.5). The instruction "Select all rows from the users table" uses "select" as a verb (technical verb, rule 1.12). Both uses are correct because the word fits both category systems.

**Systems (Rust ownership, C memory)**

Systems documentation describes resource management and safety guarantees. Common violations:

- "The drop of the guard happens at end of scope" → "The guard drops at end of scope"
- "The borrow of the reference prevents mutation" → "The reference borrow prevents mutation" or "The borrow prevents mutation" (borrow as technical noun, rule 1.5, when referring to the Rust borrow concept)
- "Do a clone of the Arc" → "Clone the Arc"

Rust documentation has an approved exception: the borrow checker is a named system component (technical noun, rule 1.5). "The borrow" as a concept name is correct. But "do a borrow" as an instruction is wrong — use "Borrow the value."

### Examples

> **Non-STE:** Do a compile of the source files.
>
> **STE:** Compile the source files.

> *Adapted from spec example: "Enter your password" — "enter" must be used only as a verb. Just as you cannot use "enter" as a noun in STE, you cannot use "compile" as a noun in STE-Code. "Compile" is a code-domain technical verb (category 1 a), development processes, write and modify code). The non-STE version uses "compile" as a noun, which is not permitted. The STE version uses "compile" correctly as a verb.*

> **Non-STE:** The merge of the feature branch caused a conflict.
>
> **STE:** The merge operation of the feature branch caused a conflict.

> *Adapted from spec principle: technical verbs must be used only as verbs. "Merge" is a code-domain technical verb (category 1 c), development processes, build and package). The non-STE example uses "merge" as a noun. The STE version uses "merge" as an adjective that is part of the code-domain technical noun "merge operation."*

> **STE:** Run the deploy script.

("Deploy" is a code-domain technical verb, category 1 c), development processes, build and package.)

> **STE:** The deploy completed successfully.

> *Adapted from spec example: "There are two methods to plate the ring nut (2)" — "plate" can be both a technical verb and a technical noun. Just as "plate" in the spec can be a technical verb (category 1 c), attach material) and also a technical noun (a different context), "deploy" can be both a code-domain technical verb (category 1 c), build and package) and a code-domain technical noun (category 5, infrastructure, deployment, and platforms). In the second example, "deploy" refers to a deployment event or process as a noun — it fits into a code-domain technical noun category in the same way "plate" fits into a technical noun category in the spec.*

> **Non-STE:** Execute a rollback of the migration.
>
> **STE:** Roll back the migration.

> *Principle applied: P13 — Do not use technical verbs as nouns. "Rollback" is a code-domain technical verb (category 3 b), database and storage). The non-STE version nominalizes "rollback" with a light verb "Execute." The STE version uses "roll back" as the main verb of the sentence — the approved verb "roll" plus the particle "back." If the project uses "rollback" as a compound noun (category 18, database and storage), the STE version "Run the rollback of the migration" is also correct because "rollback" then fits a technical noun category.*

> **Non-STE:** The import of the module takes approximately ten seconds.
>
> **STE:** The import operation for the module takes approximately ten seconds.

> *Principle applied: P13 — Do not use technical verbs as nouns, P1 — Use approved words from the STE-Code dictionary. "Import" is a code-domain technical verb (category 1 a), development processes, write and modify code). In the non-STE version, "import" is used as a noun. The STE version replaces it with the approved noun "operation" modified by "import" as an adjective. An alternative STE version "Importing the module takes approximately ten seconds" uses the gerund form — gerunds are permitted in descriptive text when they describe an ongoing process, but avoid them as main verbs in procedural sentences (refer to Section 3 grammar rules).*

> **Non-STE:** Make a commit of your changes before you switch branches.
>
> **STE:** Commit your changes before you switch branches.

> *Principle applied: P13 — Do not use technical verbs as nouns, P4 — Use only approved verb forms. "Commit" is a code-domain technical verb (category 2 c), system operations). The non-STE version wraps "commit" in a light verb construction "Make a commit." The STE version uses "commit" directly as the main imperative verb. In Git documentation, "a commit" as a noun (referring to a snapshot object) is correct because it is a code-domain technical noun (category 4, data structures) — this is the dual-category exception from rule 1.5 and rule 1.12.*

### Edge Cases

**Framework names that are verbs**

Some frameworks and tools have names that are also verbs. For example, React, Build (a build tool), Make (a build system), Log (a logging library), Split (an A/B testing tool). When the word refers to the tool or framework, it is a code-domain technical noun (rule 1.5) and can be used as a noun:

> **STE:** Install React in your project.
> **STE:** Make uses a Makefile to define build targets.

When the same word describes an action, it is a verb and must be used as a verb:

> **STE:** The component reacts to state changes.
> **STE:** The tool makes an executable from the source files.

Always capitalize framework names when they are proper nouns to distinguish them from the verb form.

**Git subcommands used as nouns**

Git documentation frequently uses subcommand names as both verbs and nouns. The subcommand name is a technical noun (it names a Git operation). The instruction to perform the operation uses the verb form:

> **STE:** Run `git rebase` to integrate the changes. (rebase = technical noun, a Git subcommand)
> **STE:** Rebase your branch onto main. (rebase = technical verb)

Both forms are correct if the word fits both category systems (rule 1.12 and rule 1.5). The dual use is the same pattern as the spec's "plate" example.

**Log and CLI tool output**

Generated output from tools, compilers, and linters is quoted text (technical noun category 10, rule 1.5). You cannot change the grammar of generated output. If a compiler emits "Build failed: compile error in module auth," the message contains "compile" as a noun. This is quoted text and does not violate rule 1.13 because you did not write the message.

When you summarize the tool output in your own documentation, apply rule 1.13:

> **STE:** The compiler could not compile module "auth."
> **Non-STE:** The compiler reported a compile error in module "auth."

The non-STE version uses "compile" as a noun ("a compile error"). The STE version uses "compile" as a verb ("could not compile"). If "compile error" is an established term in your project glossary, it can be a compound technical noun (rule 1.5).

**Docker and Kubernetes resource names**

Container orchestration tools use resource names that are verb-derived nouns. For example, a Kubernetes "Deployment" resource, a Docker "Build" stage. These are code-domain technical nouns (rule 1.5, category 5 — infrastructure, deployment, and platforms) because they name specific API resources. Use them as nouns:

> **STE:** The Deployment has three replicas.
> **STE:** The Build stage runs before the test stage.

When you describe the action, use the verb form:

> **STE:** Deploy the application to the cluster.
> **STE:** Build the Docker image from the Dockerfile.

**The "-ing" gerund as a noun substitute**

Technical writers sometimes use gerunds (-ing forms) as nouns to avoid the verb-as-noun violation: "The compiling of the source files takes ten seconds." While this avoids using "compile" as a noun, gerunds as sentence subjects can make text less direct. Prefer the verb form with a dummy subject or the imperative:

> **STE:** Compiling the source files takes ten seconds. (descriptive — correct but less direct)
> **STE:** It takes ten seconds to compile the source files. (preferred for descriptive text)

In procedural text, use the imperative verb directly:

> **STE:** Compile the source files. (procedural — preferred)

### Cross-References

This rule works with a network of related rules. Violations of rule 1.13 often trace to a misunderstanding of the category distinction.

| Rule | Relationship |
|------|-------------|
| **Rule 1.12** — You Can Use Verbs That You Can Include in a Technical Verb Category | Rule 1.12 defines which verbs are "technical verbs." Rule 1.13 constrains how you can use them. A word that does not fit a technical verb category under rule 1.12 cannot be misused as a noun because it is not a technical verb at all — use an approved verb instead. |
| **Rule 1.5** — You Can Use Words That You Can Include in a Technical Noun Category | Rule 1.5 defines which nouns are "technical nouns." When a word fits both a technical verb category (rule 1.12) and a technical noun category (rule 1.5), rule 1.13 permits dual use — just as the spec permits "plate" as both verb and noun. |
| **Rule 1.7** — Do Not Use Technical Nouns as Verbs | Rule 1.7 is the inverse of rule 1.13. Where rule 1.13 prevents verb→noun conversion, rule 1.7 prevents noun→verb conversion. Both rules enforce the principle that a word's category determines its grammatical role. |
| **Rule 1.4** — Use Only Approved Verb Forms and Adjective Forms | Rule 1.4 restricts which verb forms are permitted. When a technical verb is nominalized into a noun (violating rule 1.13), the noun form is often an unapproved derivation. Fixing the violation restores the approved verb form. |
| **Rule 1.10** — No Slang, Jargon, or Regional Terms | Nominalized technical verbs often become project-specific jargon ("a deploy," "a lint," "a hotfix"). If the noun form is not in a technical noun category (rule 1.5), the usage is jargon and violates both rule 1.13 and rule 1.10. |
| **STE-Code Dictionary** — Approved Words and Technical Verb/Noun Lists | The controlled terminology defines approved verbs and their approved parts of speech. When a verb is not approved, you cannot use it as a noun either. The dictionary entries for BUILD, CHECK, DO, GET, MAKE, RUN, SET, SHOW, START, STOP, and USE are particularly relevant to rule 1.13 violations. |

### Grammar Notes

**The light verb construction anti-pattern**

The most common violation of rule 1.13 is the light verb construction: a semantically weak verb (do, make, perform, execute, run, carry out) paired with a nominalized technical verb. For example:

- "Make a commit" instead of "Commit"
- "Do a compile" instead of "Compile"
- "Execute a deploy" instead of "Deploy"
- "Run a build" instead of "Build"

In English grammar, light verb constructions are grammatically correct but stylistically weak. In STE-Code, they are violations because the technical verb is used as a noun (the object of the light verb). The fix is always to use the technical verb as the main verb of the sentence.

When the light verb adds necessary semantic information, the construction can be correct if the object is a genuine code-domain technical noun (rule 1.5), not a nominalized verb:

> **STE:** Run the test suite. ("test suite" is a technical noun, category 3)
> **STE:** Do a quick check of the configuration. ("check" is an approved noun in the controlled terminology)

**Distinguishing technical verb from technical noun by category membership**

The only reliable test for whether a word can be used as a noun is the category test from rule 1.5. Ask:

1. Can this word fit into one of the 19 code-domain technical noun categories?
2. If yes, the word is a technical noun and can be used as a noun.
3. If no, the word cannot be used as a noun — even if it is common in your team's speech.

For example, "deploy" fits category 5 (infrastructure, deployment, and platforms) as a noun. "Compile" does not fit any technical noun category naturally — it is only a technical verb (category 1 a). Therefore, "the deploy" is correct and "the compile" is wrong.

**The dual-category exception: formal justification**

The ASD-STE100 spec explicitly permits dual-category words. The spec's example is "plate," which is both a technical verb (category 1 c, manufacturing processes) and a technical noun (category 1, official parts information). The spec does not require you to choose one category and forbid the other — it permits both when the context justifies the category assignment.

In STE-Code, common dual-category words include:

| Word | Technical Verb Category (Rule 1.12) | Technical Noun Category (Rule 1.5) |
|------|--------------------------------------|-------------------------------------|
| build | Category 1 c) Build and package | Category 3) Development tools |
| deploy | Category 1 c) Build and package | Category 5) Infrastructure, deployment, and platforms |
| test | Category 1 b) Test and verify code | Category 3) Development tools |
| commit | Category 2 c) System operations | Category 4) Data structures |
| merge | Category 1 c) Build and package | Category 4) Data structures |
| release | Category 1 c) Build and package | Category 5) Infrastructure, deployment, and platforms |
| patch | Category 1 a) Write and modify code | Category 4) Data structures |
| log | Category 2 c) System operations | Category 13) Runtime environments |
| import | Category 1 a) Write and modify code | Category 4) Data structures |

For each word, the noun use must refer to a concrete artifact or event that fits the noun category. "The build failed" is correct because "build" names a build artifact or process (category 3). "Do a build" is wrong because the instruction should use the verb form — the word is neither category here; it is a misused verb in a light verb construction.

**Regression test: the article test**

A simple test for verb-as-noun violations: if you can put an article (a, an, the) before the word and the sentence remains grammatical, the word is functioning as a noun. If it is a code-domain technical verb functioning as a noun, check the dual-category table above. If the word is not in the dual-category table, the usage violates rule 1.13.

Test application:

- "The compile failed" — "compile" with article → noun use → "compile" is not a dual-category word → VIOLATION
- "The build failed" — "build" with article → noun use → "build" is a dual-category word (category 3) → CORRECT
- "The import failed" — "import" with article → noun use → "import" is a dual-category word (category 4) → CORRECT
- "The lint found errors" — "lint" with article → noun use → "lint" is not a dual-category word → VIOLATION. Write "The linter found errors" (linter = technical noun, category 3).
