---
name: iterative-diff-research
description: Delegate a big git diff into an incremental written report.
---

# Iterative diff research (ad-hoc, session-long)

A delegate session is a loop. It can call read_file and terminal (git diff) and write_file and patch repeatedly. Use that to grow a document across MANY cycles instead of dumping it in one shot. The document on disk is the artifact, so checkpoint it often so partial progress survives rate-limits or max_iterations cutoff.

## Process (follow in this order, looping)

1. Establish the range. Run git diff --stat base..HEAD and git log base..HEAD --oneline. Record commit and file counts. A merge commit may reintroduce an earlier lump commit into history, so always measure from the true base tag base..HEAD, never by counting local commits.
2. Group changed paths by area (directory prefix). Examples: tools/lib, hermes/jail, benchmark, skills, docs, root Makefile/README.
3. Read real diffs per area. Use git diff base..HEAD -- path or read_file on specific files. Do NOT rely on path names or commit subjects alone. Read the code.
4. Build the document ad-hoc and incrementally. write_file the header plus skeleton section headings FIRST. After reading each area, patch or append the verified findings under the matching section. Grow it across many read-and-write cycles. NEVER produce the entire document in a single call.
5. Self-verification loop (critical). For every factual claim you write, immediately re-read the source diff to prove or disprove it. If disproved, patch the claim out or correct it. Mark any figure that comes from an in-repo doc (not the diff) as a document claim, not a measured fact.
6. No fabrication. Never invent metrics, test counts, or numbers. If a detail cannot be verified from the diff, describe it only at the level of commit subject plus path.
7. Close. Print a summary with sections produced, number of files whose diffs you actually read, final path, and line count.

## Pitfalls
- Rate limits and max_iterations cut sessions short, so checkpoint the file frequently. Write a little, patch a little, so progress is on disk rather than only in context.
- Do not depend on tmp research inputs that may be deleted between runs; derive everything from git diff.
- A delegate is a leaf. It cannot call delegate_task, clarify, or memory. Do the whole research itself.
- Keep claims scoped to what the diff shows. A repository or infra release that does not change the canonical standard should say so explicitly and verify it with git diff --stat base..HEAD -- standard-path.

## Output contract
- Single markdown file at the requested path, for example .agents/tmp/REPOSITORY-1.2.0.md.
- Header must state the tag family, what it was measured against, and that it is a DRAFT (not committed, tagged, or pushed).
- Draft only. Do NOT git commit, git tag, or git push. Writing the file is the whole deliverable.
