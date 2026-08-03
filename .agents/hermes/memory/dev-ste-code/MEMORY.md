<person> — maintains the `<github-org>` GitHub org: a family of repos (STE-Code, <repo-b>, <repo-c>, <repo-d>, …) that deliberately share cross-repo conventions (prettier.config.js, requirements.txt, lychee link-check config) borrowed from one another.
§
STE-Code / release-notes workflow preferences (durable):
1. Research or migration tasks that touch sibling repos are research-only: observe and read, take notes, and do not write adaptation code until explicitly instructed.
2. Use delegate_task to produce or write output; use a poll worker (local background process) for research or observation. Pick the correct one for the job.
3. The multi-stage notes pipeline follows an explicit interjection protocol: research → interject to verify against git ground truth → composer → interject to verify → assistant writes. Never trust delegate self-reports.
4. Delegates routinely hit API timeouts (HTTP 524/429) and die at max_iterations. Design work to survive: write output incrementally in small batches, and always re-verify the deliverable on disk afterward.
5. Provide informative change-summaries with file counts, commit counts, and line counts, but do not create tags or releases frequently.
6. Keep STANDARD (wording-only) releases untouched; preserve the STANDARD vs REPOSITORY release-family split.
7. Keep documents visually uniform across a set even when content differs: whitespace-rich structured markdown with one fact per line, a blank line between sections, consistent #/##/### headings, tables for tabular data, bullets for lists, and blockquotes for caveats.
