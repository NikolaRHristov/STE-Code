---
id: ste-code-user
version: "1.0"
tokens: ~900
use-when: Human-readable introduction for new contributors who have never heard of STE
source: Adapted from ASD-STE100 Issue 9 (January 2025), published by the AeroSpace and Defence Industries Association of Europe (ASD), Brussels, Belgium. © ASD, 2025 — All rights reserved. STE is a European Union Trade Mark (No. 017966390). STE-Code is an independent adaptation not endorsed by ASD. For the authoritative standard, visit asd-ste100.org.
---

# STE-Code — A Friendly Introduction

## What Is STE-Code?

STE-Code is a simple way to write software documentation that anyone can read.
It is based on ASD-STE100, a controlled-language standard that the aerospace
industry has used since 1986 to make aircraft manuals safe and clear for
non-native English speakers around the world. STE-Code brings the same idea to
code: README files, API docs, comments, error messages, and changelogs should be
so clear that no developer ever has to guess what you meant.

## The Five Ideas That Matter Most

**Use plain, approved words.** Instead of reaching for the fanciest verb in your
vocabulary, check the synonym table. Write "use" instead of "utilize." Write
"start" instead of "initiate." Write "get" instead of "retrieve." The approved
word is almost always shorter and easier to understand.

**Pick one name and stick to it.** If your project has a component called
`AuthService`, call it `AuthService` everywhere. Do not call it the "auth
module" on one page and the "login handler" on another. One concept gets one
name across the entire document.

**Keep sentences short.** Limit procedural sentences to 20 words and descriptive
sentences to 25 words. When a sentence is too long, break it into two. Short
sentences are easier to read, translate, and scan.

**Use active voice when you give instructions.** Write "Run the migration"
instead of "The migration should be run." Write "Click the save button" instead
of "The save button must be clicked." Active voice tells the reader exactly who
does what.

**Say what you mean, not what sounds clever.** No hacker jargon, no cultural
metaphors, no regional slang. Do not write "nuke the database" or "the service
went belly-up." Write "delete all database records" or "the service stopped."
Be literal. Be boring. Be understood.

## Two Examples

### Example 1: A README instruction

Before (not STE-Code):

> Leverage the config endpoint to retrieve and subsequently display the current
> system state in the dashboard.

After (STE-Code):

> Use the `/config` endpoint to get the system state. The dashboard shows the
> state.

What changed? "Leverage" became "use." "Retrieve" became "get." "Display"
became "shows." The long sentence became two short ones.

### Example 2: An API description

Before (not STE-Code):

> The performDataSync function initiates a comprehensive reconciliation process
> that validates and updates all customer records across the entire distributed
> data store hierarchy.

After (STE-Code):

> `performDataSync` compares customer records across all data stores. It checks
> each record. It applies the necessary updates.

What changed? "Initiates a comprehensive reconciliation process" became
"compares." "Validates" became "checks." "Across the entire distributed data
store hierarchy" became "across all data stores." One monster sentence became
three clear ones.

## Quick Checklist

Before you publish docs, check:

- [ ] Did you use plain approved words (not "utilize," "leverage,"
  "initiate")?
- [ ] Does each concept have one name across the whole document?
- [ ] Are your procedural sentences 20 words or fewer?
- [ ] Do your instructions use active voice ("Run X" not "X should be run")?
- [ ] Did you remove jargon, metaphors, and slang?
- [ ] Did you put code-block language tags on every fenced code block?

## Attribution

STE-Code is an independent adaptation of ASD-STE100 Issue 9 (January 2025),
published by the AeroSpace and Defence Industries Association of Europe (ASD),
Brussels, Belgium. Copyright © ASD, 2025 — All rights reserved. STE is a
European Union Trade Mark (No. 017966390). STE-Code is not endorsed by ASD. For
the authoritative standard, visit asd-ste100.org.
