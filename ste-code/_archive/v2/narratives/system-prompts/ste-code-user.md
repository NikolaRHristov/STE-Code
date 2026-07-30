# STE-Code — User Guide

> You are a developer, technical writer, or team member who wants to write cleaner code documentation. This guide teaches you the STE-Code standard in plain language.

---

## What Is STE-Code?

STE-Code is a writing standard for code documentation. It is adapted from ASD-STE100 — the aerospace industry's Simplified Technical English standard, used since 1986 to make aircraft maintenance manuals readable by non-native English speakers worldwide.

STE-Code applies the same idea to code: README files, API docs, inline comments, commit messages, error messages, and changelogs should be clear, unambiguous, and consistent — readable by any developer regardless of English proficiency.

---

## The Core Idea

Instead of writing whatever words feel natural, you use a controlled vocabulary. Every term has a fixed type and a fixed meaning. When you want to say "fetch the data", you write "read the data" because `read` is the approved verb for data retrieval operations. When you want to say "nuke the database", you write "delete the database records".

This sounds restrictive. In practice it makes documentation dramatically easier to read, translate, and process by LLMs.

---

## The 5 Rules You Need Most

**1. Use approved words.** Check the synonym table first. If your word is in the left column, use the right column instead.

**2. One name per thing.** Pick one name for each component and use it everywhere. Never call the same service `AuthService`, `auth module`, and `login handler` in the same document.

**3. Short sentences.** Max 20 words for steps and procedures. Max 25 words for descriptions. When a sentence is longer, split it.

**4. Active voice in steps.** Write "Run the migration." not "The migration should be run."

**5. Name your code blocks.** Write ` ```javascript ` not just ` ``` `. Always.

---

## Quick Synonym Reference

| Instead of... | Write... |
|---------------|----------|
| fetch, get, retrieve, grab | `read` |
| set, configure, assign | `write` |
| check, verify, confirm | `test` |
| make, create, generate | `build` |
| change, modify, edit | `update` |
| fix, resolve, correct | `repair` |
| show, print, output | `display` |
| start, begin, launch | `start` |
| stop, end, kill, terminate | `stop` |
| send, transmit | `send` |
| find, locate, discover | `search` |
| remove, erase | `delete` |
| keep, save | `store` |

---

## BREAKING, DEPRECATED, NOTE

STE-Code uses three notice types for important information:

**BREAKING** — An action that causes data loss, API incompatibility, or a security problem. Always include the version and the migration path.

**DEPRECATED** — Something that still works but will be removed. Always include the version when it will be removed.

**NOTE** — Extra information that helps understanding. Use sparingly.

---

## How to Extend the Standard

If your project uses a term that is not in the vocabulary (e.g., a proprietary framework), add it to `data/vocabulary/exceptions/domain-extensions.json` using the vocabulary entry format. Tag it with your domain. Submit it for review before using it in production documentation.

---

## Full Reference

- Full system prompt (for LLMs): `narratives/system-prompts/ste-code-full.md`
- All rules: `core/rules/`
- Vocabulary: `data/vocabulary/`
- Synonym table: `data/synonyms/synonym-table.json`
