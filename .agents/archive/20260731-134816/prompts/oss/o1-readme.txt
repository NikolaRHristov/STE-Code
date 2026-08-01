TASK: Write the root-level README.md for the STE-Code open-source project. This is the GitHub landing page.

OUTPUT: <project-root>/README.md

CONTEXT FILES TO READ:
- ste-code/artifacts/README.md (project overview)
- ste-code/artifacts/ste-code-distilled-system-prompt.txt (first ~30 lines for summary)
- ste-code/README.md (pipeline overview)

REQUIRED SECTIONS:
1. **Project title + badge row**: License (MIT), pipeline status, version
2. **What is STE-Code?** — 2-3 sentences. Adapts ASD-STE100 aerospace standard into code documentation. 53 rules, 19 categories, 14 principles.
3. **Quick Example** — before/after code documentation transformation
4. **Pipeline Architecture** — ASCII diagram showing 5-stage pipeline
5. **Quick Start** — 3 code blocks: Ollama one-liner, Python snippet, direct file usage
6. **Repository Structure** — tree view of key directories
7. **Credits & Attribution** — credit ASD-STE100, ASD Europe, the original Issue 9 authors. Link to www.asd-europe.org. Note that STE-Code is an independent adaptation.
8. **License** — MIT License reference
9. **Citation** — BibTeX entry for academic use
10. **Links** — GitHub repo, ASD-STE100 source, poolside/laguna-s-2.1:free

CRITICAL FACTS:
- 19 categories (NOT 22)
- 53 writing rules + 4 GR rules
- Model: poolside/laguna-s-2.1:free
- Source: ASD-STE100 Issue 9, January 2025, ASD Europe, Brussels
- 434 pages adapted
- Original STE trademark: European Union Trade Mark No. 017966390
- © ASD, 2025 — All rights reserved (original spec)
- STE-Code is an independent adaptation, not endorsed by ASD

Include links: https://github.com/NikolaRHristov/Manual, https://www.asd-europe.org, https://asd-ste100.org

Output ONLY the README.md content. No commentary.
