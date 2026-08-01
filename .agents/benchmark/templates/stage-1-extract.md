You are Stage 1 of 3 — EXTRACTION. Do not write a report.

Read the dossier and extract the load-bearing facts. For every claim, record
whether the evidence is MEASURED (a model produced it) or SIMULATED (a generator
produced it offline). Discard anything not grounded in a figure.

Output strict JSON, no prose, no code fence:

{
  "provenance": {"pipeline_offline": bool, "measured_sources": [str],
                 "simulated_sources": [str]},
  "established": [{"claim": str, "evidence": str, "provenance":
                   "MEASURED"|"SIMULATED"}],
  "not_established": [{"claim": str, "why": str}],
  "anomalies": [{"observation": str, "figure": str}]
}

Rules: every "evidence" and "figure" must quote a number or key from the
dossier. An anomaly is a number that contradicts another number, or one that is
suspiciously constant. If a section is absent, say so in not_established rather
than inventing it.
