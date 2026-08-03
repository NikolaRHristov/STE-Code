---
name: applying-ste-code
description:
    Use when writing or rewriting documentation to the STE-Code standard. Loads
    the right level artifact and applies the rules.
---

# Applying STE-Code to your documentation

Use this when the user asks you to write, review, or rewrite documentation to
the STE-Code standard: comments, docstrings, error messages, commit messages,
API documentation, changelogs, or configuration files.

## 1. Find the checkout

The STE-Code repository is read-only in this profile. Locate it before you
start:

```bash
ls ste-code/artifacts/llms.txt
```

If that path does not resolve, ask the user where the checkout is. Do not guess,
and do not reconstruct rules from memory — the standard on disk is the
authority.

## 2. Load the right level

Each level is one plain-text file. A higher level is stricter and costs more
context.

| Level | File                                           |  Tokens | Use when                              |
| :---: | ---------------------------------------------- | ------: | ------------------------------------- |
|  -2   | `ste-code/artifacts/level-2/system-prompt.txt` |   ~1.2K | A quick pass, principles only         |
|   1   | `ste-code/artifacts/level1/system-prompt.txt`  |  ~14.5K | **Start here.** Rules plus templates  |
|   3   | `ste-code/artifacts/level3/system-prompt.txt`  |  ~94.7K | Full dictionary and all 54 rules      |
|   5   | `ste-code/artifacts/level5/system-prompt.txt`  | ~133.8K | The complete standard with provenance |

Read the level file with `read_file` and apply it. Level 1 is the default
choice; move up only when a rule you need is missing.

## 3. Apply the standard

Work through the text and apply the rules rather than describing them:

- Active voice. One instruction per sentence.
- Approved vocabulary. Replace an unapproved term with its synonym-table entry.
- A table in place of three paragraphs of parallel prose.
- No hedging: delete "basically", "simply", "just", "should probably".
- Keep sentences at or under 20 words.

Look up the specific rule in `ste-code/final/rules/` when you need the exact
wording. The files are named `a-sec<N>-rule<X>.<Y>.md`.

## 4. Write to the user's project, never to the checkout

The jail refuses a write into the STE-Code tree, and that refusal is correct.
Write the result into the user's own repository.

If the user launched Hermes from inside the checkout, they have no writable
project root. Tell them to restart from their own project directory:

```bash
cd ~/my-project
env -u HERMES_HOME \
	HERMES_PROFILE=ste-code \
	HERMES_HOME=~/.hermes/profiles/ste-code \
	hermes --tui
```

## 5. Report what you changed

Give the user a short table: the original text, the rewrite, and the rule number
you applied. Cite the rule only when the change is not self-evident.

## Pitfalls

- **Do not invent rules.** If you cannot find it in `ste-code/final/rules/`, say
  so instead of asserting a rule number.
- **Do not fetch anything.** Network access is off in this profile by design.
- **Do not edit the checkout** to "fix" a rule you disagree with. Report the
  disagreement to the user; changing the standard is `dev-ste-code` work.
