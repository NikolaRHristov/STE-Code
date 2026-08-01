# Provenance — STE-Code pipeline stages


| Stage | Source dir | Role |
|---|---|---|
| A Extraction | ste-code/extracted/ | PDF spec -> structured pages |
| B Refinement | ste-code/refined/ | formatted dict/rule markdown |
| C Grouping | ste-code/grouped/ | semantic slice+concat of pages |
| D Adaptation | ste-code/adapted/ | code-domain rule rewrite |
| G Enrichment | ste-code/final/rules/ | cross-refs + traceability |
| E Extension | ste-code/extensions/ | code-domain vocabulary gap-fills |
| References | .agents/reference/ | vendor/community vocab (catalogued) |

Consolidated into ste-code/final/ by assemble_final.py.
