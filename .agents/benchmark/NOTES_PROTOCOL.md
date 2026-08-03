# Notes Protocol

## Purpose

This addendum to `CONTRACT.md` defines how the colours of the adversarial
harness tell each other things without ever calling each other. A note is a
durable, addressed, acknowledged message on disk. It is evidence, not chatter:
every note carries the artifact ids that justify it, so a reader verifies the
claim instead of trusting it. Authors of any colour module read this before they
emit or consume a note.

## Footprint

Resolved from `notes.*` and `handshake.*` in
`.agents/benchmark/config/harness.json`.

| Kind    | Value                                                            |
| ------- | ---------------------------------------------------------------- |
| Inputs  | `<base>/notes/index.json`, prior `<note_id>.json` records        |
| Outputs | `<base>/notes/<note_id>.json` (immutable), appended `index.json` |
| Outputs | `handshake.attack_brief` — the WHITE→BLACK brief                 |
| Outputs | `handshake.verdicts` — BLACK's verdicts                          |
| Agent   | none; note handling is offline and deterministic                 |

## Usage

Notes are written by the colour modules, not by hand. Inspect a run's
correspondence with:

    python3 .agents/benchmark/notes.py --help
    python3 .agents/benchmark/selftest.py

## Behaviour

- Each colour writes one note per file under `<base>/notes/` and appends to
  `index.json` for cheap scanning.
- A note is never edited after it is written; a correction is a new note that
  supersedes the old one by id.
- A note with `expects_ack: true` must be answered by an `acknowledgement` or
  `rebuttal` note carrying `in_reply_to`.
- PURPLE surfaces unacknowledged notes older than `notes.stale_after_rounds` as
  `stale_notes` in the stitch report, so silence is visible.
- WHITE hands BLACK an attack brief of falsifiable hypotheses; BLACK tests them.
- BLACK partitions the corpus into two arms and never draws a conclusion from
  the data that produced it.
- All note writes go through the shared `ste_io` helpers and resolve through
  `ste_paths`.

## Configuration

Knobs live in `.agents/benchmark/config/harness.json` under `notes.*` and
`verification.*`; the shared agent defaults live in
`.agents/config/defaults.yaml`. None is hardcoded in a module.

| Key                                            | Governs                                        |
| ---------------------------------------------- | ---------------------------------------------- |
| `notes.colours`                                | Valid `from_colour` and `to_colour` values     |
| `notes.kinds`                                  | Valid note kinds                               |
| `notes.ack_dispositions`                       | `accepted`, `deferred`, `rejected`             |
| `notes.stale_after_rounds`                     | When PURPLE reports a note as stale            |
| `notes.require_evidence`                       | Whether a note without evidence is rejected    |
| `verification.partition_strategies`            | The split-half strategies BLACK may pick       |
| `verification.default_strategy`                | Default partition, `stratified_half`           |
| `verification.overfit_tolerance_pct`           | Gap above which a remedy counts as overfitting |
| `verification.min_arm_size`                    | Below this an arm is `underpowered`            |
| `verification.split_seed`                      | Makes the partition deterministic              |
| `handshake.notes_dir`, `handshake.notes_index` | Storage names                                  |

### Why notes exist

The colours are independent processes. They cannot pass objects, share memory,
or await each other's return values. They still have things to tell each other:

- RED knows which schematic it believed should have worked, and why.
- BLUE knows which relocation of a payload broke a defense that held elsewhere.
- PURPLE sees cross-colour contradictions that neither side sees alone.
- WHITE knows which remedy it adopted and what it expects that remedy to fix.
- BLACK needs all of the above to attack the conclusion rather than the
  configuration.

### Storage

```
<base>/notes/
    <note_id>.json          one note per file, immutable once written
    index.json              append-only index for cheap scanning
```

### Note record

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

### Acknowledgement

An acknowledgement states one of:

- `accepted` — the receiver acted on it; `action_taken` says how.
- `deferred` — understood, not actionable this round; `reason` says why.
- `rejected` — the receiver disputes it; `rebuttal` carries counter-evidence.

### Who writes what

| From   | To     | Typical kind | Content                                                     |
| ------ | ------ | ------------ | ----------------------------------------------------------- |
| RED    | BLUE   | handoff      | "ledger for round N is ready; these techniques are novel"   |
| RED    | PURPLE | claim        | "this schematic should have escaped and did not"            |
| BLUE   | RED    | request      | "relocate this payload to `nested`; it survived only there" |
| BLUE   | WHITE  | claim        | "resistance is placement-driven, not technique-driven"      |
| PURPLE | all    | warning      | "RED's attack count and BLUE's probe count disagree"        |
| WHITE  | BLACK  | handoff      | the attack brief                                            |
| BLACK  | all    | rebuttal     | "your result does not survive the split-half test"          |

### The WHITE to BLACK handoff

WHITE is the only colour with a cross-round, cross-variant model of why things
fail. That model is exactly what an attacker needs to discredit the benchmark,
so WHITE writes it down and hands it over:

```
kind:     handoff
to:       black
subject:  attack brief
body:     the weakest links in RED's coverage, BLUE's probe construction,
          and PURPLE's aggregation — stated as exploitable hypotheses
evidence: the lessons and patterns that support each hypothesis
```

Each hypothesis is falsifiable: "if X were true, the reported result would be
inflated by about Y".

### BLACK verdicts

| Verdict        | Meaning                                                              |
| -------------- | -------------------------------------------------------------------- |
| `confirmed`    | the result reproduces under BLACK's independent construction         |
| `inflated`     | the reported number is optimistic; BLACK gives a corrected estimate  |
| `deflated`     | the reported number is pessimistic, usually a scoring artifact       |
| `unsound`      | the result does not survive; the methodology is broken for this cell |
| `underpowered` | too few observations to support the claim                            |

### Split-half A/B verification

The corpus is partitioned into two arms. The A arm is the derivation set:
WHITE's remedies and BLUE's probes may be built from it. The B arm is the
verification set: untouched until the claim is fixed, then evaluated once.

| Strategy             | Split rule                                       | Detects                    |
| -------------------- | ------------------------------------------------ | -------------------------- |
| `random_half`        | stable hash of case id, mod 2                    | ordinary sampling noise    |
| `stratified_half`    | balanced within each (technique, placement) cell | confounding by cell        |
| `technique_disjoint` | half the techniques in A, the rest in B          | technique overfitting      |
| `placement_disjoint` | half the placements in A, the rest in B          | placement overfitting      |
| `temporal_half`      | early rounds in A, late rounds in B              | drift across rounds        |
| `variant_holdout`    | one variant held out entirely                    | whether a lesson transfers |

BLACK reports the A-arm effect, the B-arm effect, the gap, and whether the gap
exceeds `verification.overfit_tolerance_pct`. Any conclusion drawn from the
derivation arm alone is labelled `derivation-only` and is never presented as a
measured result.

## Failure modes

- A note without evidence is rejected when `notes.require_evidence` is true.
- An unacknowledged note past `notes.stale_after_rounds` appears as
  `stale_notes` in the stitch report; the sending colour keeps working and does
  not block.
- An arm smaller than `verification.min_arm_size` yields the `underpowered`
  verdict rather than a number.
- A superseded note that is edited in place breaks diffability; write a new note
  instead.
- A partition run with a different `verification.split_seed` is not comparable
  with earlier runs.

## See also

- `CONTRACT.md` — genericity rules, handshake protocol, record shapes
- `WORKER_BRIEF.md` — session starter for every harness worker
- `docs/capsule-sequenced-pipeline.md` — capsule scheduling specification
- `config/harness.json` — the profile document
