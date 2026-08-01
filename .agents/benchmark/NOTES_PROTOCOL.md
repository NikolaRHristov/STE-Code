# Notes Protocol — inter-colour correspondence

An addendum to `CONTRACT.md`. It defines how the colours talk to each other
without ever calling each other.

## Why notes

The colours are independent processes. They cannot pass objects, share memory,
or await each other's return values. But they *do* have things to tell each
other:

- RED knows which schematic it believes should have worked and why.
- BLUE knows which relocation of a payload broke a defense that held elsewhere.
- PURPLE sees cross-colour contradictions neither side can see alone.
- WHITE knows which remedy it adopted and what it expects that remedy to fix.
- BLACK needs all of the above in order to attack the *conclusion* rather than
  the configuration.

A note is a durable, addressed, acknowledged message on disk. It is evidence,
not chatter: every note carries the artifact ids that justify it, so a reader
can verify the claim instead of trusting it.

## Storage

```
<base>/notes/
    <note_id>.json          one note per file, immutable once written
    index.json              append-only index for cheap scanning
```

A note is never edited after it is written. A correction is a new note that
supersedes the old one by id.

## Note record

```
id              stable: <from>-<to>-<variant>-<round>-<seq>
schema_version  int
from_colour     red | blue | purple | white | black
to_colour       red | blue | purple | white | black | all
variant, round  scope of the observation
kind            claim | warning | request | acknowledgement | rebuttal | handoff
subject         one-line summary
body            the reasoning, in full
evidence        {escape_ids[], probe_ids[], remedy_ids[], artifact_paths[]}
confidence      0..1 — how strongly the sender holds this
expects_ack     bool
supersedes      note id or null
created_at      iso8601
```

## Acknowledgement

A note with `expects_ack: true` must be answered by a note of kind
`acknowledgement` (or `rebuttal`) carrying `in_reply_to`. An acknowledgement
states one of:

- `accepted` — the receiver acted on it; `action_taken` says how
- `deferred` — understood, not actionable this round; `reason` says why
- `rejected` — the receiver disputes it; `rebuttal` carries counter-evidence

Unacknowledged notes older than a configurable age are surfaced by PURPLE as
`stale_notes` in the stitch report. Silence is visible, not invisible.

## Who writes what

| From | To | Typical kind | Content |
|---|---|---|---|
| RED | BLUE | handoff | "ledger for round N is ready; these techniques are novel this round" |
| RED | PURPLE | claim | "this schematic should have escaped and did not — suspect scoring, not defense" |
| BLUE | RED | request | "relocate this payload to `nested`; it survived there and nowhere else" |
| BLUE | WHITE | claim | "resistance is placement-driven, not technique-driven, for this cluster" |
| PURPLE | all | warning | "RED's attack count and BLUE's probe count disagree for this cell" |
| WHITE | BLACK | handoff | **the attack brief** — see below |
| BLACK | all | rebuttal | "your result does not survive the split-half test" |

## The WHITE → BLACK handoff

WHITE is the only colour with a cross-round, cross-variant model of *why*
things fail. That same model is exactly what an attacker would need to discredit
the benchmark. So WHITE writes it down deliberately and hands it to BLACK:

```
kind:    handoff
to:      black
subject: attack brief
body:    the weakest links in RED's coverage, BLUE's probe construction,
         and PURPLE's aggregation — stated as exploitable hypotheses
evidence: the lessons and patterns that support each hypothesis
```

Each hypothesis is a falsifiable claim of the form "if X were true, the reported
result would be inflated by roughly Y". BLACK's job is to test them.

## BLACK: the verifier

BLACK does not attack the configuration under test. It attacks the **claim** the
other three colours jointly produce. Its findings are verdicts on the benchmark
itself:

| Verdict | Meaning |
|---|---|
| `confirmed` | the result reproduces under BLACK's independent construction |
| `inflated` | the reported number is optimistic; BLACK gives the corrected estimate |
| `deflated` | the reported number is pessimistic (usually a scoring artifact) |
| `unsound` | the result does not survive; the methodology is broken for this cell |
| `underpowered` | too few observations to support the claim at all |

## Split-half A/B verification

BLACK's primary instrument. The case corpus is partitioned into two halves and
each half is used for a different purpose, so that no conclusion is ever drawn
from the same data that produced it.

Partition strategies (all deterministic given a seed):

| Strategy | Split rule | Detects |
|---|---|---|
| `random_half` | stable hash of case id, mod 2 | ordinary sampling noise |
| `stratified_half` | balanced within each (technique, placement) cell | confounding by cell composition |
| `technique_disjoint` | half the techniques in A, the rest in B | technique overfitting — a remedy that only fixes what it was shown |
| `placement_disjoint` | half the placements in A, the rest in B | placement overfitting |
| `temporal_half` | early rounds in A, late rounds in B | drift, and remedies that only work on the round they were derived from |
| `variant_holdout` | one variant held out entirely | whether a lesson transfers across configurations |

The A arm is the **derivation** set: WHITE's remedies and BLUE's probes may be
built from it. The B arm is the **verification** set: it is untouched until the
claim is fixed, then evaluated once. A remedy that helps on A and not on B is
overfitting, and BLACK says so with the measured gap.

BLACK reports, per claim: the A-arm effect, the B-arm effect, the gap, and
whether the gap exceeds the tolerance. Any conclusion drawn from the derivation
arm alone is labelled `derivation-only` and never presented as a measured
result.
