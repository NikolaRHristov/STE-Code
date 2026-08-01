# Rule 1.14 — Use American English Spelling Unless Other Official Directives Tell You Differently

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.14](ste-code/grouped/), Rule 1.14

## Original Rule

**Rule 1.14** Use American English spelling unless other official directives tell you differently.

Use the spelling specified in the STE dictionary (American English spelling). Use a different spelling only if other technical publication specifications, style guides, contracts, or other official directives are applicable.

Examples:

("Fiber" is American English spelling.)

("Color" is American English spelling.)

If there is quoted text that has British English spelling, for example on a computer screen, do not change the spelling. Keep the quoted text as it is. Refer to Rule 8.6 which tells you how to use quoted texts correctly.

## STE-Code Adaptation

**Rule 1.14** Use American English spelling unless other official directives tell you differently.

> **See also:** Rule 8.6 — Use Quoted Texts Correctly

Use the spelling specified in the STE-Code controlled terminology (American English spelling). Use a different spelling only if other project specifications, style guides, contracts, or other official directives are applicable.

This adapts the spec directly: the same rule applies to code documentation as it does to aerospace documentation. American English spelling is the default in both STE and STE-Code.

If there is quoted text that has British English spelling, for example in an error message, a code comment, or on a user interface, do not change the spelling. Keep the quoted text as it is. Refer to Rule 8.6 which tells you how to use quoted texts correctly.

### Examples

> **Non-STE:** The log file shows the colour of each output line.
>
> **STE:** The log file shows the color of each output line.

> *Adapted from spec example: "Color" is American English spelling, and the spec explicitly lists it as an example. The non-STE version uses the British English spelling "colour," which is not permitted. The STE version uses the American English spelling "color."*

> **Non-STE:** Initialise the variable before you use it in the loop.
>
> **STE:** Initialize the variable before you use it in the loop.

> *Adapted from spec example: "Fiber" is American English spelling. Just as the spec requires American English spelling for all technical documentation, STE-Code requires it for code documentation. "Initialize" is American English spelling. The non-STE version uses the British English spelling "initialise," which is not permitted.*

> **STE:** The terminal shows the message `Colour profile not recognised`.

> *Adapted from spec concept: if a computer screen displays text with British English spelling, you must not change the spelling of the quoted text. In STE-Code, if a terminal output or error message contains British English spelling ("Colour," "recognised"), you must keep the quoted text exactly as it is. The surrounding documentation text must use American English spelling. This is the same principle as the spec example where British spelling in quoted computer screen text is preserved.*

---

## Code-Domain Explanation

Rule 1.14 is a surface-level constraint that applies to every word in every type of code documentation. Unlike rules that govern vocabulary selection (Rule 1.1) or part of speech (Rule 1.2), Rule 1.14 governs the spelling of words that are already selected. It is the final orthographic check before documentation is complete.

The rule has consequences beyond cosmetic consistency. British English spellings can cause confusion in technical contexts where spelling differences create ambiguity. For example, "meter" (American) is a measuring device; "metre" (British) is a unit of length. In code documentation, "meter" always refers to a measurement component, and "metre" would be an error.

### README Files

README files are the first document a new contributor reads. Inconsistent spelling between American and British English signals a lack of editorial control. README files must use American English spelling throughout, including in headings, bullet points, code comments within README code blocks, and link text.

Common README violations involve the -ise/-ize suffix pair. Words that end in "-ise" in British English end in "-ize" in American English: "initialise" becomes "initialize," "organise" becomes "organize," "recognise" becomes "recognize." The -yse/-yze pair follows the same pattern: "analyse" becomes "analyze," "paralyse" becomes "paralyze."

Example — README installation section:

> **Non-STE:** Organise your environment variables in a `.env` file. The application analyses this file at startup.
>
> **STE:** Organize your environment variables in a `.env` file. The application analyzes this file at startup.
> *(P14 applied: "organise" → "organize"; "analyse" → "analyze")*

### API Documentation

API documentation is often generated from source code annotations. When the source annotations use British English spelling and a generation tool produces the final output, both the source and the output must follow Rule 1.14. This is especially important for public APIs, where British English spellings in parameter descriptions or return value documentation can confuse non-native English speakers who learned American English spelling conventions.

Parameter names and endpoint paths are code-domain technical nouns (Rule 1.5, category 10). If a parameter name contains a British English spelling, you must not change it in the code. But the prose description of that parameter must use American English spelling.

Example — OpenAPI description:

> **Non-STE:** `colour_scheme` — The colour scheme to apply to the dashboard. Accepted values: "light", "dark".
>
> **STE:** `colour_scheme` — The color scheme to use for the dashboard. Accepted values: "light", "dark".
> *(P14 applied: "colour" → "color" in prose; parameter name `colour_scheme` preserved as quoted text)*

### Docstrings and Inline Comments

Docstrings and inline comments are the documentation closest to the source code. They are read by developers who work in many different spelling environments. American English spelling in docstrings gives a consistent reading experience regardless of the developer's native language.

British English spellings in docstrings often come from developers whose locale defaults to British English. Common violations include "behaviour" (British) instead of "behavior" (American), "centre" instead of "center," and "defence" instead of "defense."

Example — Python docstring:

> **Non-STE:** """Centre the text in the terminal window. Returns the centred string."""
>
> **STE:** """Center the text in the terminal window. Gives the centered string."""
> *(P14 applied: "centre" → "center"; "centred" → "centered"; P1 also applied: "returns" → "gives")*

### Commit Messages

Commit messages are short and indexable. British English spellings in commit messages create friction during search: a developer who searches for "color" will not find commits that say "colour." Consistent American English spelling makes commit history searchable across teams with different language backgrounds.

Common commit message violations:

| British | American | Context |
|---------|----------|---------|
| colour | color | UI, terminal, theming |
| behaviour | behavior | feature descriptions, bug reports |
| organise | organize | restructuring, refactoring |
| recognise | recognize | pattern matching, parsing |
| analyse | analyze | profiling, data processing |
| defence | defense | security fixes |

Example — commit message:

> **Non-STE:** fix: correct colour parsing behaviour in the analytics module
>
> **STE:** fix: correct color parsing behavior in the analytics module
> *(P14 applied: "colour" → "color"; "behaviour" → "behavior")*

### Error Messages

Error messages that the development team writes are documentation. They must use American English spelling. Error messages from third-party libraries, language runtimes, or operating systems are quoted text (Rule 1.5, category 10). If a third-party error message uses British English spelling, you must not change it.

When you write error messages for your own software, apply Rule 1.14 consistently. An error message that says "colour" in one place and "color" in another is a quality defect.

Example — application error message:

> **Non-STE:** Error: The licence key is not recognised. Please contact your administrator.
>
> **STE:** Error: The license key is not recognized. Speak to your administrator.
> *(P14 applied: "licence" (noun) → "license"; "recognised" → "recognized"; P1 applied: "contact" → "speak to")*

> **Non-STE:** OSError: [Errno 2] No such file or directory: '/etc/program/colour_profiles.cfg'
> **STE (third-party):** OSError: [Errno 2] No such file or directory: '/etc/program/colour_profiles.cfg'
> *(No change: the error message is quoted text from the operating system. The British spelling "colour" is preserved exactly as the system produces it.)*

---

## Paradigm-Specific Guidance

Rule 1.14 applies uniformly to all paradigms because spelling is language-level, not paradigm-level. But each paradigm has its own vocabulary of common British English violations that appear in documentation because of historical spelling patterns in the paradigm's community.

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses many words that end in -or/-our and -ize/-ise. The OOP community has historically been split between American and British spelling conventions. Some Java standard library methods and C# framework APIs use British English spellings in their names (for example, `java.awt.Color` uses American spelling, but some older Java libraries use British spelling). This creates documentation challenges.

**Common OOP documentation spelling violations:**

| British | American | OOP Context |
|---------|----------|-------------|
| behaviour | behavior | class behavior, method behavior, object behavior |
| colour | color | UI component color, syntax highlighting color |
| initialise | initialize | object initialization, lazy initialization |
| serialise | serialize | object serialization, data serialization |
| optimise | optimize | performance optimization, query optimization |
| parametrise | parameterize | parameterized types, parameterized tests |
| customise | customize | custom behavior, custom implementation |

Example — Java class documentation:

> **Non-STE:** The `CacheManager` class is responsible for the initialisation and serialisation of cached objects. It optimises memory usage through customisable eviction behaviour.
>
> **STE:** The `CacheManager` class is responsible for the initialization and serialization of cached objects. It optimizes memory usage through customizable eviction behavior.
> *(P14 applied: "initialisation" → "initialization"; "serialisation" → "serialization"; "optimises" → "optimizes"; "customisable" → "customizable"; "behaviour" → "behavior")*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional programming documentation has fewer spelling violations than OOP documentation because the functional community adopted American English spelling conventions early. But Elixir, which has a strong European user base, is an exception. Elixir documentation and library names sometimes use British English spellings (for example, "behaviour" is the name of a language construct in Elixir, and it uses British spelling).

**Guidance points for functional documentation:**

- The word "behaviour" is used in British English spelling as a language keyword in Elixir. When referring to the Elixir `@behaviour` module attribute, use the British spelling because it is quoted text (the actual code uses that spelling). But when describing the concept in prose, use the American English spelling "behavior."
- Haskell documentation uses "centre" in some older texts. Modern Haskell documentation should use "center."
- Clojure documentation follows American English spelling conventions.
- Rust documentation follows American English spelling conventions.

Example — Elixir module documentation:

> **Non-STE:** This module defines a custom behaviour for plug initialisation. Modules that implement this behaviour must provide an `init/1` callback.
>
> **STE:** This module defines a custom `@behaviour` for plug initialization. Modules that implement this `@behaviour` must give an `init/1` callback.
> *(P14 applied: "initialisation" → "initialization"; `@behaviour` preserved as code keyword; P1 applied: "provide" → "give")*

### Procedural (C, Go, Bash)

Procedural documentation has the fewest British English spelling violations because the procedural community is predominantly American. But specialized domains within procedural programming — especially embedded systems, networking, and telecommunications — have historically used British English because of their European origins.

**Common procedural documentation spelling violations:**

| British | American | Procedural Context |
|---------|----------|-------------------|
| licence | license | software license, license key |
| defence | defense | defense programming, defense in depth |
| cancelled | canceled | canceled operations, canceled signals |
| traveller | traveler | traveler pattern in process management |

Example — C library documentation:

> **Non-STE:** The licence key must be validated before the defence mechanisms are initialised.
>
> **STE:** The license key must be checked before the defense mechanisms are initialized.
> *(P14 applied: "licence" → "license"; "defence" → "defense"; "initialised" → "initialized"; P1 applied: "validated" → "checked")*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation often includes British English spellings because many declarative tools (Terraform, Kubernetes, Ansible) are developed by international teams with European contributors. But the official documentation for these tools uses American English spelling, and STE-Code documentation must follow the same convention.

**Guidance points for declarative documentation:**

- Kubernetes documentation uses American English spelling ("behavior," "color," "organize").
- Terraform documentation uses American English spelling. HashiCorp is an American company.
- SQL keywords do not have spelling variants (SELECT, INSERT, UPDATE are the same in all English locales). But SQL comments and documentation strings do.
- YAML is a data serialization format. Documentation about YAML must use American English spelling.

Example — Terraform module documentation:

> **Non-STE:** This module centralises the organisation of network policies. It also synchronises security groups across regions.
>
> **STE:** This module centralizes the organization of network policies. It also synchronizes security groups across regions.
> *(P14 applied: "centralises" → "centralizes"; "organisation" → "organization"; "synchronises" → "synchronizes")*

### Systems (Rust Ownership, C Memory Management)

Systems documentation has a vocabulary of spelling-sensitive words related to memory and hardware. Words like "defense," "license," "meter," and "analog" have American English spellings that differ from their British English equivalents. Using the wrong spelling can create ambiguity in technical contexts.

**Common systems documentation spelling violations:**

| British | American | Systems Context |
|---------|----------|----------------|
| analogue | analog | analog signal, analog input |
| metre | meter | memory meter, CPU meter |
| defence | defense | memory defense, defense in depth |
| cancelled | canceled | canceled memory allocation |
| traveller | traveler | traveler pattern in garbage collection |

Example — Rust systems documentation:

> **Non-STE:** The memory metre shows the current heap usage. The defence mechanisms prevent double-free errors and cancelled allocations from corrupting the heap.
>
> **STE:** The memory meter shows the current heap usage. The defense mechanisms prevent double-free errors and canceled allocations from corrupting the heap.
> *(P14 applied: "metre" → "meter"; "defence" → "defense"; "cancelled" → "canceled")*

---

## Extended Examples

Each example pair below shows a real code documentation scenario with a British English spelling violation, the STE-Code compliant rewrite, which principle was applied, and an explanation of the fix.

### Example 1 — API Reference: Parameter Description

> **Non-STE:** @param {string} colour — The colour of the notification badge. Accepts any valid CSS colour value.
>
> **STE:** @param {string} color — The color of the notification badge. Accepts any valid CSS color value.
>
> **Principle applied:** P14 (use American English spelling: "colour" → "color")
> **Explanation:** Both occurrences of "colour" in the parameter documentation use British English spelling. The American English spelling "color" is required. Note that CSS property names (for example, `background-color`) use American English spelling natively, so the documentation is
> now also consistent with the API it documents.

### Example 2 — README: Architecture Overview

> **Non-STE:** The service-oriented architecture centralises request handling through a single API gateway. This organisation minimises latency and maximises throughput.
>
> **STE:** The service-oriented architecture centralizes request handling through a single API gateway. This organization minimizes latency and maximizes throughput.
>
> **Principle applied:** P14 (use American English spelling: "centralises" → "centralizes"; "organisation" → "organization"; "minimises" → "minimizes"; "maximises" → "maximizes")
> **Explanation:** Four words in two sentences use the British English -ise suffix. The American English -ize suffix is required for all four. This example shows how a single paragraph can accumulate many spelling violations when a British English locale is used. The -ise/-ize pattern is the most frequent source of Rule 1.14 violations in code documentation.

### Example 3 — Docstring: Function Behavior Description

> **Non-STE:** /** Analyses the input data and recognises patterns. Returns an object modelling the recognised patterns. */
>
> **STE:** /** Analyzes the input data and recognizes patterns. Gives an object that models the recognized patterns. */
>
> **Principle applied:** P14 (use American English spelling: "analyses" (verb) → "analyzes"; "recognises" → "recognizes"; "recognised" → "recognized"); P1 (use approved words: "returns" → "gives")
> **Explanation:** Three words use the British English -yse/-ise suffixes. The American English -yze/-ize suffixes are required. "Modelling" is also a British English spelling variant (American: "modeling"), but the rewrite avoids it by restructuring the sentence. The docstring now uses American English spelling throughout.

### Example 4 — Commit Message: Configuration Change

> **Non-STE:** chore: standardise ESLint configuration across all packages and synchronise with the monorepo
>
> **STE:** chore: standardize ESLint configuration across all packages and synchronize with the monorepo
>
> **Principle applied:** P14 (use American English spelling: "standardise" → "standardize"; "synchronise" → "synchronize")
> **Explanation:** Two verbs in a commit message use the British English -ise suffix. The American English -ize suffix is required. Commit messages with British English spelling break search consistency across a team.

### Example 5 — Error Message: User-Facing Validation

> **Non-STE:** Validation error: The programme cannot recognise the file format. The file may have been cancelled during transfer.
>
> **STE:** Validation error: The program cannot recognize the file format. The file may have been canceled during transfer.
>
> **Principle applied:** P14 (use American English spelling: "programme" → "program"; "recognise" → "recognize"; "cancelled" → "canceled")
> **Explanation:** Three British English spelling variants in a user-facing error message. "Programme" (British) refers to a television or radio broadcast in American English; "program" is the American English spelling for a computer program. "Cancelled" uses the British English double-L convention; the American English single-L "canceled" is required.

### Example 6 — Configuration File Comment

> **Non-STE:** # The log level controls the verbosity of output. Set to "debug" to
> # analyse the full request/response lifecycle, including serialisation
> # behaviour and connection pool utilisation.
> **STE:** # The log level controls the verbosity of output. Set to "debug" to
> # analyze the full request/response lifecycle, including serialization
> # behavior and connection pool usage.
>
> **Principle applied:** P14 (use American English spelling: "analyse" → "analyze"; "serialisation" → "serialization"; "behaviour" → "behavior"; "utilisation" → "usage"); P1 (use approved words: "utilisation" is not approved; "usage" is the approved noun form of "use")
> **Explanation:** Four British English spelling violations in a three-line configuration comment. Three are -yse/-ise suffix violations. The fourth is "behaviour," which uses the -our ending. "Utilisation" is both a British English spelling (American: "utilization") and an unapproved word under P1. The rewrite uses "usage," which is the approved noun form.

---

## Edge Cases

The following scenarios show where the rigid application of Rule 1.14 requires careful judgment because of conflicts with code-domain technical terms, framework conventions, or other official directives.

### Edge Case 1: Framework or Library Name That Uses British English Spelling

**Scenario:** A widely used framework or library has a name that uses British English spelling. Examples include:

- Elixir's `Behaviour` module (the language keyword uses British spelling)
- Python's `argparse` module historically accepted British English spellings in some parameter names
- Some npm packages use British English spelling in their package names (for example, `colours`, `centre-align`)
- The `centre` attribute in some older HTML/CSS specifications

**Guidance:** Framework names, library names, and package names are code-domain technical nouns (Rule 1.5, categories 3 and 1). You must write them with their official spelling, even when that spelling uses British English. The framework author chose the spelling, and changing it would create confusion.

When you write prose about a framework that uses British English spelling in its name, the prose must use American English spelling:

> **Non-STE:** The `ColourPicker` component uses the `colour` library for colour space conversions.
>
> **STE:** The `ColourPicker` component uses the `colour` library for color space conversions.
> *(Framework names preserved; prose uses American English spelling)*

This creates a visual inconsistency, but it is the correct approach. The inconsistency signals to the reader that the British English words are technical names, not prose vocabulary.

### Edge Case 2: Code Keyword That Uses British English Spelling

**Scenario:** A programming language keyword or standard library function uses British English spelling. Examples include:

- Elixir: `@behaviour`, `defexception` (exception names may use British spelling)
- Python: `os.error` and older standard library error messages may use British English
- C++: Some older Boost libraries use British English spelling in function names
- CSS: Some older CSS properties used British English spelling (for example, `colour` was proposed but never adopted; `centre` was used in some early drafts)

**Guidance:** When the British English spelling is part of the code (a keyword, a function name, a class name), it is code-domain technical text. Preserve it exactly as it appears in the code. The surrounding documentation prose must use American English spelling.

> **Non-STE:** The `@behaviour` callback initialises the module's state.
>
> **STE:** The `@behaviour` callback initializes the module state.
> *(P14 applied: "initialises" → "initializes"; `@behaviour` preserved as code keyword)*

Extreme case: when a language keyword and a documentation word are adjacent and use different spelling conventions:

> **STE:** The `@behaviour` defines the behavior of the module.
> *(Both spellings coexist: `@behaviour` is a code keyword, "behavior" is prose)*

This is visually awkward but technically correct. Avoid the awkwardness by restructuring when possible:

> **STE:** The module behavior is set by the `@behaviour` callback.
> *(Separation reduces the visual clash)*

### Edge Case 3: Generated Documentation from British English Tools

**Scenario:** Documentation generation tools (Sphinx, JSDoc, Doxygen, godoc) may produce output that contains British English spellings. This happens when the tool uses British English default templates or when the tool was developed by a team in a British English locale.

**Guidance:** Rule 1.14 applies to documentation that a human writes or reviews. When a generation tool adds British English boilerplate (for example, "Generated by Sphinx. Copyright © 2024. All rights reserved.") you cannot control it without customizing the tool's templates.

The following approach is recommended:

1. For public-facing API documentation, customize the generation tool's templates to use American English spelling.
2. For internal documentation, accept the generated boilerplate as-is unless it causes confusion.
3. Write all source annotations (docstrings, comments, descriptions) in American English spelling. The generated output will inherit the correct spelling for the content you control.

> **Ste (acceptable for internal docs):** *Generated by Sphinx. All rights reserved. Licence: MIT.*
> *(The boilerplate "Licence" is from the tool's British English template. It is acceptable for internal documentation.)*

> **STE (preferred for public docs):** *Generated by Sphinx. All rights reserved. License: MIT.*
> *(The template was customized to use American English spelling. This is preferred for public documentation.)*

### Edge Case 4: Internationalization (i18n) and Localization (l10n) Strings

**Scenario:** A software application has internationalization (i18n) strings that must support both American English and British English locales. The American English locale file must use American English spelling. The British English locale file must use British English spelling.

**Guidance:** Localization files are quoted text when referenced in documentation. The documentation prose around them must use American English spelling. The content of the files must be preserved as-is.

> **STE:** The `en-GB.json` locale file contains `"colour": "Colour"`. The `en-US.json` locale file contains `"color": "Color"`.
> *(Both locale strings are preserved as-is. The documentation prose uses American English spelling: "contains," "file.")*

When you write the American English locale file for your application, Rule 1.14 applies to that file as documentation. The British English locale file is written for British English users and falls under the "official directive" exception to Rule 1.14: the locale specification requires British English spelling.

### Edge Case 5: Official Directive to Use British English

**Scenario:** A project has an official style guide or contributing guide that requires British English spelling. For example, a project sponsored by a British organization or a project in a British English locale (for example, UK government software) may mandate British English spelling.

**Guidance:** Rule 1.14 states "unless other official directives tell you differently." An official project style guide that mandates British English spelling is an official directive. In this case, you must use British English spelling throughout the project's documentation.

> **NOTE:** When a project uses British English spelling by official directive, it is not using STE-Code. STE-Code requires American English spelling. But the STE-Code specification acknowledges that official directives override the default. This is the same exception mechanism that the original ASD-STE100 provides.

> **Recommendation:** If the project has no official directive, use American English spelling. If the project has an official directive for British English spelling, document this exception in the project's CONTRIBUTING.md file and apply British English spelling consistently throughout.

---

## Cross-References

Rule 1.14 is the final orthographic constraint in Section 1 (Words). It interacts with several other rules:

| Rule | Title | Relationship to Rule 1.14 |
|------|-------|---------------------------|
| **Rule 1.1** | Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs | Rule 1.14 constrains the spelling of words that pass Rule 1.1. You must first select the correct word (Rule 1.1) and then spell it with American English (Rule 1.14). |
| **Rule 1.5** | You Can Use Words That You Can Include in a Technical Noun Category | Technical nouns that use British English spelling in their official names must be preserved. Rule 1.14 makes an exception for quoted text and proper names. |
| **Rule 1.6** | Use a Non-Approved Word Only When It Is a Technical Noun | Non-approved words used as technical nouns may carry British English spelling from their source. Rule 1.14 requires American English spelling for prose but preserves quoted text spelling. |
| **Rule 1.8** | Use Standard, Well-Known Technical Nouns | Standard technical nouns have a canonical spelling. Rule 1.8 and Rule 1.14 both require using the standard form: Rule 1.8 requires using the well-known term, and Rule 1.14 requires the American English spelling of it. |
| **Rule 1.10** | No Slang, Jargon, or Regional Terms | British English spellings can be a form of regional variation. Rule 1.10 prohibits regional terms, and Rule 1.14 extends this prohibition to regional spellings. |
| **Rule 1.11** | One Term Per Concept — Be Consistent | Consistent spelling is part of consistent terminology. If you use "color" in one section and "colour" in another, you violate both Rule 1.11 (inconsistent terminology) and Rule 1.14 (non-American spelling). |
| **Rule 8.6** | Use Quoted Texts Correctly | Rule 8.6 governs how to present quoted text in documentation. Rule 1.14 requires that quoted text with British English spelling must not be changed — it must be preserved as-is. Rule 8.6 gives the formatting and presentation rules for such quoted text. |

**Dictionary reference:** See `a-dictionary.md` for the full STE-Code controlled terminology. All approved words in the dictionary use American English spelling. If a word's approved spelling differs from a British English variant you are used to, the dictionary is the authority.

**Categories reference:** See `a-categories.md` for the 19 code-domain technical noun categories. Category 10 (Quoted Text) is the primary exception mechanism for British English spellings in code documentation.

---

## Grammar Notes

### The Spelling Classification Model

Rule 1.14 divides all words in code documentation into three spelling classes:

1. **Prose Words — American English Only:** Every word in the descriptive and procedural prose of code documentation must use American English spelling. This includes headings, sentences, bullet points, table content, and figure captions. There are no exceptions for prose words.

2. **Quoted Text — Preserved As-Is:** Words that appear as quoted text (Rule 1.5, category 10) must be preserved with their original spelling. This includes error messages from third-party libraries, terminal output, UI labels, file paths, and code keywords. When quoted text uses British English spelling, you must not change it.

3. **Code-Domain Technical Nouns — Official Spelling:** Technical nouns (Rule 1.5, all categories) must use their official spelling. When the official spelling uses British English (for example, the `colour` npm package, the `@behaviour` Elixir keyword), you must preserve that spelling. The surrounding prose must use American English spelling.

### The -ize/-ise Suffix Rule

The most frequent Rule 1.14 violation in code documentation is the -ize/-ise suffix pair. The rule is:

- Use -ize (American English): initialize, serialize, optimize, organize, recognize, synchronize, standardize, parameterize, customize, authorize, characterize, prioritize, utilize → (not approved; use "use" per P1), minimize, maximize, centralize, visualize.

- Do not use -ise (British English): initialise, serialise, optimise, organise, recognise, synchronise, standardise, parametrise, customise, authorise, characterise, prioritise, utilise, minimise, maximise, centralise, visualise.

There are no exceptions to this rule in STE-Code prose. The -ise suffix is never permitted in documentation prose.

**NOTE:** The word "size" (meaning dimensions) uses -ize in both American and British English. "Size" is not a -ize suffix verb — it is a standalone noun. The verb "size" (to measure or adjust the size) also uses -ize in both dialects. These words are not affected by the -ize/-ise rule.

### The -or/-our Suffix Rule

The second most frequent Rule 1.14 violation is the -or/-our suffix pair in nouns:

- Use -or (American English): color, behavior, flavor, humor, labor, neighbor, rumor, harbor, honor, vapor, rigor.

- Do not use -our (British English): colour, behaviour, flavour, humour, labour, neighbour, rumour, harbour, honour, vapour, rigour.

**Exception:** The word "contour" uses -our in both American and British English. It is not an -or/-our alternation word.

### The -er/-re Suffix Rule

The -er/-re alternation affects a small set of words:

- Use -er (American English): center, theater, liter, meter (measuring device), fiber, caliber.

- Do not use -re (British English): centre, theatre, litre, metre (unit of length), fibre, calibre.

**NOTE:** "Meter" and "metre" have different meanings in American English. "Meter" is a measuring device (a parking meter, a voltage meter). "Metre" is not an American English word. For the unit of length, American English also uses "meter" (a two-meter cable). In code documentation, "meter" always refers to a measuring or monitoring component (a memory meter, a CPU meter). "Metre" should not appear in American English code documentation.

### The -l/-ll Doubling Rule

British English doubles the final "l" before -ed, -ing, -er, -or suffixes in words where American English uses a single "l":

- Use single -l (American English): canceled, canceling, traveler, traveling, modeled, modeling, labeled, labeling, fueled, fueling, signaled, signaling.

- Do not use double -ll (British English): cancelled, cancelling, traveller, travelling, modelled, modelling, labelled, labelling, fuelled, fuelling, signalled, signalling.

**Exception:** Words where the stress falls on the final syllable always double the consonant in both dialects: "compelled," "compelling," "rebelled," "rebelling." These are not Rule 1.14 violations.

### Words with Different Spelling in Both Dialects

Some words have completely different spellings in American and British English beyond suffix patterns:

| British | American | Code Documentation Context |
|---------|----------|---------------------------|
| programme | program | computer program, program file |
| licence (noun) | license (noun and verb) | license key, license agreement |
| defence | defense | defense programming, defense in depth |
| offence | offense | offense-detection rules, security offense |
| pretence | pretense | rarely used in code documentation |
| practise (verb) | practice (verb and noun) | best practice, practice exercise |
| analyse | analyze | analyze data, code analysis |
| paralyse | paralyze | rarely used in code documentation |
| catalogue | catalog | service catalog, API catalog |
| dialogue | dialog | dialog box, dialog window |
| analogue | analog | analog signal, analog input |
| judgement | judgment | rarely used in code documentation |
| manoeuvre | maneuver | rarely used in code documentation |
| plough | plow | rarely used in code documentation |

### Words with the Same Spelling in Both Dialects

Some words that are sometimes mistakenly hyper-corrected to American English actually have the same spelling in both dialects:

- "Address" (not "adress")
- "All" (not "al")
- "Committee" (not "comittee")
- "Disappoint" (not "dissapoint")
- "Necessary" (not "neccessary")
- "Occurrence" (not "occurrance")
- "Parallel" (not "paralel")
- "Recommend" (not "reccomend")

These are not Rule 1.14 issues — they are general spelling errors that would violate any English spelling standard.

### The Quoted Text Exception: Grammar of Preservation

Rule 1.14 states that quoted text with British English spelling must be preserved. This creates a specific grammatical context: quoted text is orthographically isolated from the surrounding prose. The prose uses American English spelling. The quoted text uses its original spelling. The boundary is marked by quotation marks, backticks, code blocks, or other formatting conventions (Rule 8.6).

When a quoted British English word appears adjacent to an American English prose word, the reader sees two different spelling conventions in the same sentence. This is intentional: it signals that one word is a technical reference and the other is documentation prose.

> **STE:** The `Colour` class manages color profiles for the application.
> *(`` `Colour` `` is a code reference; "color" is prose)*

This visual distinction is a feature, not a defect. It helps the reader distinguish between technical names and explanatory prose.

### Historical Note: ASD-STE100 Precedent

In ASD-STE100 Issue 9, Rule 1.14 is a short but important rule. The original specification recognizes that aerospace documentation is international and that American English spelling is the international standard for technical English. The rule provides the spelling standard for the entire STE dictionary.

The original specification gives two examples: "Fiber" (American) and "Color" (American). These examples were chosen because they are frequent words in aerospace documentation and have well-known British English variants ("fibre," "colour"). STE-Code extends this principle to code documentation, where the frequency of -ize/-ise, -or/-our, and -er/-re alternations is high because of the domain's vocabulary.

The original specification acknowledges that official directives can override Rule 1.14. This exception mechanism is preserved in STE-Code. When a project has an official style guide that requires British English spelling, that guide is an official directive and Rule 1.14 does not apply. The project is then outside the scope of STE-Code for spelling, though all other STE-Code rules still apply.

### Practical Enforcement

Rule 1.14 is the easiest STE-Code rule to enforce with automated tools. Spelling checkers can flag British English spellings automatically. The following approach is recommended for enforcing Rule 1.14 in a project:

1. Configure the project's spell checker to use American English (en-US).
2. Add a pre-commit hook that runs a spell check on all documentation files.
3. Use a CI/CD pipeline step that rejects documentation with British English spellings.
4. Maintain a project-specific dictionary of approved technical nouns with British English spellings (for example, `colour` as an npm package name) so the spell checker does not flag them.
5. Require code review for documentation changes, with Rule 1.14 as a review checklist item.

Automated enforcement prevents the most common Rule 1.14 violations before they enter the project's documentation. Human review is still necessary for the edge cases (framework names, code keywords, quoted text).
