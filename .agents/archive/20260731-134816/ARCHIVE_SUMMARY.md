# Archive Summary

Date: 2026-07-31T10:48:16Z

## Contents

| Directory | Files Archived |
|-----------|---------------|
| prompts/ | 227 |
| tmp/ | 82 |
| telemetry/ | 51 (JSON) |
| feedback/ | 1 |

## Notes

This archive contains session data from the pre-reorganization phase.
All scripts have been moved to the new hierarchical structure under
.agents/tools/{lib,shared,runners,extraction,refinement,maintenance,quality,benchmark}/

The extraction pipeline will be re-run from scratch using the new
extract_batch.py with 1800s timeout and improved path resolution.
