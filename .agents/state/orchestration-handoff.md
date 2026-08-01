# STE-Code Phase C remediation — orchestration handoff (updated)

## ROOT CAUSES (verified)
1. 35 refined dict files were displaced ~2 files / ~8 pages from their extracted
   source (shift distribution {-3:1, -2:36, 0:21}). Re-running fixed 10/35 so far
   (r052 r053 r054 r056 r057 r072 r073 r082 r083 r084 — confirmed via the
   CORRECTED headword regex below).
2. **Some extracted sources are EMPTY of entries**: e.g. extracted/w055-p217-220.md
   contains ONLY `# Page 217/218 of 434` headers and NO dictionary table. So the
   refiner for r055 had no correct source and emitted stale E-words. The
   displacement is partly an EXTRACTION defect, not only refinement.
3. Concurrent LLM workers correctly capped at 3 (the "5" earlier was the TUI
   gateway double-counted — pids 88344/12748 are the Hermes TUI, not refine).

## CORRECTED AUDIT REGEX (the earlier ones had TWO bugs: space after |, and
## double-pipe ||**word). Use this for all verification:
  def hw(path):
      t=open(path,encoding='utf-8',errors='ignore').read(); s=set()
      for m in re.finditer(r'^\|+\s*\*{0,2}\s*([A-Za-z][A-Za-z\-]*)\s*\(', t, re.M): s.add(m.group(1).lower())
      for m in re.finditer(r'^#{3,4}\s+\*{0,2}([A-Za-z][A-Za-z\-]*)\s*\(', t, re.M): s.add(m.group(1).lower())
      return s
  overlap(n) = len(hw(refined/r{n}-*)) & hw(extracted/w{n}-*)) / len(hw(extracted/w{n}-*))
  PASS if overlap>=0.5 AND extracted source is non-empty.

## CONFLICT workers: 054 055 056 072 073 074 075 076 077 078 079 081 082 083 084
## 085 086 087 089 090 091 092 093 094 095 096 097 098 099 101 102 103 104 105 106
## FIXED so far (10): 052 053 054 056 057 072 073 082 083 084
## STILL TODO (25): 055 074 075 076 077 078 079 081 085 086 087 089 090 091 092
## 093 094 095 096 097 098 099 101 102 103 104 105 106
## NOTE: 055 blocked by EMPTY extracted w055 — must re-extract or repair w055 first.

## PHASE EXECUTION CONTRACT (user directive)
- Main agent (me) only PLANS + VERIFIES. Never runs a phase myself.
- Each phase = ONE delegate that EXECUTES it (poll workers, never scripts).
- After each phase delegate returns, main agent verifies with the corrected regex
  / parity gate, then approves the next phase.
- Phases in order: (A) finish refinement + fix empty extracted sources,
  (B) dict table normalizer + verifier (Fix B/D), (C) re-run grouping --verify,
  (D) phase-d adapt, (E) phase-e extend, (F) phase-f artifacts.

## Do NOT edit: grouped/, adapted/, extended/, artifacts/ while another session
## owns them. refined/ is being fixed by the refinement delegate.
