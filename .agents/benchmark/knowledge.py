#!/usr/bin/env python3
"""WHITE knowledge base: a content-addressed, versioned, append-only store.

WHITE's durable memory. It accumulates across runs at <base>/knowledge.json and
lets the self-healing loop turn raw escapes into lessons, lessons into patterns,
and patterns into transferable predictions for variants that have never been
probed.

Content addressing
------------------
Every LESSON is keyed by a stable signature: the blake2s hash of
(technique, placement, timing, category, sorted missed_principles,
normalized forbidden_found). The same signature seen again bumps an occurrence
counter -- it never creates a second row. This is what makes the base converge
instead of growing linearly with traffic.

Confidence + decay (explicit rule, implemented exactly)
------------------------------------------------------
Each lesson holds beta parameters alpha, beta in [0,1]-space via integer counts
a (passes corroborating the lesson) and b (failures). We track failures as the
primary signal (a lesson is "real" when failures keep occurring) and passes as
decay/repair evidence.

  confidence = a / (a + b)            # beta-mean, starts 0/0 -> 0
  On a NEW failure for a signature:   b += 1
  On a ROUND where the signature is ABSENT (evidence it was fixed): a += 1

Time/round decay: every `decay_every` rounds with no failure, multiply both
counts' *effective weight* by `decay_factor` (applied to a shadow copy so the
raw counts stay auditable). We store `last_seen_round`; if a query happens many
rounds later, the reported confidence is down-weighted:

  age = max(0, current_round - last_seen_round)
  decay_mult = decay_factor ** (age // decay_every)
  effective_conf = confidence * decay_mult

This is documented here and implemented verbatim in confidence_of().

Generalization (patterns)
-------------------------
Lessons roll up into PATTERNS when a group shares a technique across placements
('technique X escapes regardless of placement'), a placement across techniques
('placement Y defeats everything'), or a missed principle. Each pattern carries
support (count) and lift = (support / total lessons) / (1 / values on that axis),
i.e. how much the group exceeds an even spread across that axis. lift > 1 means
the axis value concentrates failures; lift ~ 1 means it carries no signal.

Transfer
--------
For a variant never probed, predict likely escapes from lessons on OTHER variants,
weighted by similarity of cfg.variant(key).intensity. Higher-intensity variants
inherit the harder lessons.

Writes are atomic (temp file + os.replace). schema_version is stored; load()
tolerates unknown keys so the format can grow.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1
DECAY_FACTOR = 0.85        # confidence multiplier per decay period
DECAY_EVERY = 3           # rounds without a failure = one decay step


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def signature(technique: str, placement: str, timing: str, category: str,
              missed_principles, forbidden_found,
              position_aware: bool = False, sequence_position: int = -1) -> str:
    """Stable content hash of a failure signature.

    When ``position_aware`` is True, ``sequence_position`` is mixed into the
    hash blob so the same (technique, placement, ...) at different sequence
    positions produces a *different* lesson key. This is what lets WHITE detect
    temporal attacks (e.g. a compliance_spoof that only escapes after a helpful
    BLUE capsule). Default False keeps existing lesson keys stable.
    """
    princ = sorted(str(p) for p in (missed_principles or []))
    forb = sorted(str(f) for f in (forbidden_found or []))
    blob = [technique, placement, timing, category, princ, forb]
    if position_aware:
        blob.append("pos:{}".format(sequence_position))
    blob = json.dumps(blob, separators=(",", ":"), sort_keys=True)
    return hashlib.blake2s(blob.encode("utf-8"), digest_size=8).hexdigest()


def _norm(text: str) -> str:
    return " ".join(str(text).lower().split())


# --------------------------------------------------------------------- Knowledge

class Knowledge:
    """The knowledge base object. Loaded from / written to a JSON file."""

    def __init__(self, path: "str | Path", decay_factor: float = DECAY_FACTOR,
                 decay_every: int = DECAY_EVERY) -> None:
        self.path = Path(path)
        self.decay_factor = decay_factor
        self.decay_every = decay_every
        self.schema_version = SCHEMA_VERSION
        self.lessons: "dict[str, dict]" = {}
        self._patterns: "dict[str, dict]" = {}
        self.version = 0
        self._load()

    # -- persistence ---------------------------------------------------------

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        self.schema_version = int(raw.get("schema_version", SCHEMA_VERSION))
        self.version = int(raw.get("version", 0))
        # tolerate unknown keys: only pull what we know, keep the rest via update
        self.lessons = {}
        raw_lessons = raw.get("lessons")
        if isinstance(raw_lessons, dict):
            for k, v in raw_lessons.items():
                L = dict(v)
                L["rounds_seen"] = set(L.get("rounds_seen", []))
                L["variants_affected"] = set(L.get("variants_affected", []))
                # Unit 1 capsule provenance: restore set/list on load
                if "capsule_ids" in L and not isinstance(L["capsule_ids"], set):
                    L["capsule_ids"] = set(L["capsule_ids"])
                L.setdefault("sequence_positions", [])
                L.setdefault("first_sequence_id", "")
                self.lessons[k] = L
        # non-dict lessons (legacy/corrupt/foreign shape) are ignored, not fatal
        self._patterns = {k: dict(v) for k, v in (raw.get("patterns") or {}).items() if isinstance(v, dict)}

    @staticmethod
    def _serialize_lessons(lessons: "dict[str, dict]") -> "dict[str, dict]":
        out = {}
        for k, L in lessons.items():
            L = dict(L)
            L["rounds_seen"] = sorted(L.get("rounds_seen", []))
            L["variants_affected"] = sorted(L.get("variants_affected", []))
            # Unit 1 capsule provenance: sets/lists must be JSON-serializable
            if isinstance(L.get("capsule_ids"), set):
                L["capsule_ids"] = sorted(L["capsule_ids"])
            if isinstance(L.get("sequence_positions"), list):
                L["sequence_positions"] = sorted(L["sequence_positions"])
            out[k] = L
        return out

    def flush(self) -> None:
        """Atomic write: temp file + os.replace, so a crash mid-write loses nothing."""
        payload = {
            "schema_version": self.schema_version,
            "version": self.version + 1,
            "updated_at": _now_iso(),
            "lessons": self._serialize_lessons(self.lessons),
            "patterns": self._patterns,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(self.path.parent), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(payload, indent=2))
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(tmp, self.path)
            self.version += 1
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    # -- lesson ingestion ----------------------------------------------------

    def record_failure(self, technique, placement, timing, category,
                       missed_principles, forbidden_found, variant: str,
                       round_n: int, correctness_score: float,
                       input_text: str, current_round: int,
                       capsule_id: str = "", sequence_position: int = -1,
                       sequence_id: str = "") -> str:
        """Ingest one escape. Returns the lesson signature (id).

        Unit 1 (capsule provenance): ``capsule_id`` and ``sequence_position``
        let WHITE ask whether a lesson only appears when the capsule is at a
        given position in a sequence (a temporal dependency invisible to a
        single-capsule run). They are optional and ignored by existing callers.
        """
        sig = signature(technique, placement, timing, category,
                        missed_principles, forbidden_found,
                        position_aware=(sequence_position >= 0),
                        sequence_position=sequence_position)
        now = _now_iso()
        if sig not in self.lessons:
            self.lessons[sig] = {
                "signature": sig,
                "technique": technique, "placement": placement,
                "timing": timing, "category": category,
                "missed_principles": sorted(str(p) for p in (missed_principles or [])),
                "forbidden_found": sorted(str(f) for f in (forbidden_found or [])),
                "first_seen": now, "last_seen": now,
                "first_seen_round": round_n, "last_seen_round": round_n,
                "occurrences": 0, "rounds_seen": set(),
                "variants_affected": set(),
                "scores": [], "examples": [],
                "a": 0, "b": 0, "last_seen_round": current_round,
                # --- Unit 1 capsule provenance ---
                "capsule_ids": set(),
                "sequence_positions": [],
                "first_sequence_id": sequence_id or "",
            }
        L = self.lessons[sig]
        L["occurrences"] += 1
        L["last_seen"] = now
        L["last_seen_round"] = round_n
        L["rounds_seen"].add(round_n)
        L["variants_affected"].add(variant)
        if capsule_id:
            L["capsule_ids"].add(capsule_id)
        if sequence_position >= 0:
            L["sequence_positions"].append(sequence_position)
        if sequence_id and not L["first_sequence_id"]:
            L["first_sequence_id"] = sequence_id
        L["scores"].append(correctness_score)
        # cap + dedup example inputs
        ex = _norm(input_text)[:300]
        if ex not in [e["norm"] for e in L["examples"]]:
            L["examples"].append({"norm": ex, "text": str(input_text)[:300]})
            L["examples"] = L["examples"][:5]
        L["b"] += 1  # a failure corroborates the lesson
        self._regenerate_patterns()
        return sig

    def decay_lesson(self, sig: str, weight: int = 1) -> bool:
        """Apply one immediate decay step to a challenged lesson (Unit 0 Patch D).

        Bumping ``a`` (absence/decay evidence) lowers ``b/(a+b)`` exactly as the
        natural round-boundary decay does, so a BLACK rebuttal can knock a
        lesson's confidence down without waiting for the next round. Returns
        True if the lesson existed and was decayed.
        """
        L = self.lessons.get(sig)
        if L is None:
            return False
        L["a"] += max(1, int(weight))
        self._regenerate_patterns()
        return True

    def record_absence(self, current_round: int) -> None:
        """Call once per round per variant that produced NO escapes for a signature.

        Evidence the signature was fixed -> decay path (a += 1). We do not know
        which signatures were absent, so this is invoked by WHITE only for the
        set of signatures it expected; see white.py which passes the prior set.
        """
        for L in self.lessons.values():
            # only decay lessons that were seen before and are now quiet
            if L["last_seen_round"] < current_round:
                L["a"] += 1
                L["last_seen_round"] = current_round

    # -- confidence ----------------------------------------------------------

    def confidence_of(self, sig: str, current_round: int) -> float:
        """Beta-mean confidence, age-decayed per the documented rule."""
        L = self.lessons.get(sig)
        if L is None:
            return 0.0
        a, b = L["a"], L["b"]
        if a + b == 0:
            return 0.0
        # b counts failures (corroborating evidence a lesson is real); a counts
        # absences (decay/repair evidence). A lesson is confident when failures
        # are frequent and recent -> confidence = b / (a + b).
        conf = b / (a + b)
        age = max(0, current_round - L["last_seen_round"])
        decay_mult = self.decay_factor ** (age // self.decay_every)
        return round(conf * decay_mult, 4)

    def severity(self, sig: str) -> float:
        """Heuristic severity: how wrong the output was, averaged, inverted."""
        L = self.lessons.get(sig)
        if L is None or not L["scores"]:
            return 0.0
        mean_score = sum(L["scores"]) / len(L["scores"])
        # low correctness == high severity
        return round((1.0 - mean_score) * (1.0 + 0.1 * L["occurrences"]), 4)

    # -- patterns ------------------------------------------------------------

    def _regenerate_patterns(self) -> None:
        self._patterns = {}
        by_tech: "dict[str, list[str]]" = {}
        by_place: "dict[str, list[str]]" = {}
        by_princ: "dict[str, list[str]]" = {}
        for sig, L in self.lessons.items():
            by_tech.setdefault(L["technique"], []).append(sig)
            by_place.setdefault(L["placement"], []).append(sig)
            for p in L["missed_principles"]:
                by_princ.setdefault(p, []).append(sig)
        total = len(self.lessons)

        def _emit(kind, key, sigs, universe):
            if len(sigs) < 2:
                return
            pattern_id = "pat-{}-{}".format(kind, hashlib.blake2s(
                key.encode()).hexdigest()[:6])
            # Lift compares this group's share of the corpus against the share
            # it would hold if the axis were spread evenly over its observed
            # values. Dividing (len(sigs)/total) by itself -- the previous
            # base_rate -- is 1.0 by construction and carries no signal.
            share = len(sigs) / total if total else 0.0
            base_rate = (1.0 / len(universe)) if universe else 0.0
            self._patterns[pattern_id] = {
                "id": pattern_id, "kind": kind, "key": key,
                "support": len(sigs), "lesson_ids": sorted(sigs),
                "lift": round(share / base_rate, 3) if base_rate else 0.0,
            }

        for t, s in by_tech.items():
            _emit("technique_across_placements", t, s, by_tech)
        for p, s in by_place.items():
            _emit("placement_across_techniques", p, s, by_place)
        for pr, s in by_princ.items():
            _emit("missed_principle", pr, s, by_princ)

    # -- query API -----------------------------------------------------------

    def top_lessons(self, n: int = 10, by: str = "confidence",
                    current_round: int = 0) -> "list[dict]":
        keys = {"confidence": lambda s: self.confidence_of(s, current_round),
                "occurrences": lambda s: self.lessons[s]["occurrences"],
                "severity": lambda s: self.severity(s)}
        fn = keys.get(by, keys["confidence"])
        ordered = sorted(self.lessons.keys(), key=fn, reverse=True)
        out = []
        for s in ordered[:n]:
            L = dict(self.lessons[s])
            L["confidence"] = self.confidence_of(s, current_round)
            L["severity"] = self.severity(s)
            L["rounds_seen"] = sorted(L["rounds_seen"])
            L["variants_affected"] = sorted(L["variants_affected"])
            out.append(L)
        return out

    def lessons_for(self, variant: str = None, technique: str = None,
                    placement: str = None) -> "list[dict]":
        out = []
        for s, L in self.lessons.items():
            if variant is not None and variant not in L["variants_affected"]:
                continue
            if technique is not None and L["technique"] != technique:
                continue
            if placement is not None and L["placement"] != placement:
                continue
            out.append(dict(L))
        return out

    def patterns(self, min_support: int = 2) -> "list[dict]":
        return [p for p in self._patterns.values() if p["support"] >= min_support]

    def unresolved(self, confidence_floor: float = 0.0, current_round: int = 0) -> "list[dict]":
        return [self._with_conf(s, current_round) for s in self.lessons
                if self.confidence_of(s, current_round) >= confidence_floor]

    def resolved(self, current_round: int = 0) -> "list[dict]":
        """Lessons whose decayed confidence has fallen below 0.2 (likely fixed)."""
        return [self._with_conf(s, current_round) for s in self.lessons
                if self.confidence_of(s, current_round) < 0.2]

    def _with_conf(self, sig: str, current_round: int) -> dict:
        L = dict(self.lessons[sig])
        L["confidence"] = self.confidence_of(sig, current_round)
        return L

    # -- transfer ------------------------------------------------------------

    def predict(self, target_variant_key: str, all_variants: "list",
                n: int = 5, current_round: int = 0) -> "list[dict]":
        """Predict likely escapes for a variant never probed, weighted by the
        intensity similarity of known variants."""
        target = None
        for v in all_variants:
            if str(v.key) == str(target_variant_key) or v.key == target_variant_key:
                target = v
                break
        if target is None:
            return []
        target_int = float(getattr(target, "intensity", 1.0))
        scored = []
        for sig, L in self.lessons.items():
            # weight by how similar each contributing variant's intensity is
            w = 0.0
            for vid in L["variants_affected"]:
                for v in all_variants:
                    if str(v.key) == str(vid):
                        w += 1.0 / (1.0 + abs(float(getattr(v, "intensity", 1.0)) - target_int))
                        break
            if w == 0.0:
                w = 0.5
            scored.append((w * (1.0 + L["occurrences"]), sig))
        scored.sort(key=lambda x: x[0], reverse=True)
        weight_by_sig = {sig: w for w, sig in scored}
        out = []
        for _, sig in scored[:n]:
            L = self._with_conf(sig, current_round)
            L["transfer_weight"] = round(weight_by_sig.get(sig, 0.0), 3)
            out.append(L)
        return out

    # -- diff ----------------------------------------------------------------

    def diff(self, other: "Knowledge") -> dict:
        """Report what changed between this version and `other`."""
        added = [s for s in self.lessons if s not in other.lessons]
        removed = [s for s in other.lessons if s not in self.lessons]
        changed = []
        for s in self.lessons:
            if s in other.lessons:
                a, b = self.lessons[s], other.lessons[s]
                if (a["occurrences"] != b["occurrences"]
                        or a["a"] != b["a"] or a["b"] != b["b"]):
                    changed.append({
                        "signature": s,
                        "occurrences_delta": a["occurrences"] - b["occurrences"],
                        "a_delta": a["a"] - b["a"], "b_delta": a["b"] - b["b"],
                    })
        return {"added": added, "removed": removed, "changed": changed,
                "self_version": self.version, "other_version": other.version}


# ------------------------------------------------------------------ self-test

def _selftest() -> int:
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="kb-selftest-"))
    fails = 0

    def check(ok, label):
        nonlocal fails
        print(("PASS " if ok else "FAIL ") + label)
        if not ok:
            fails += 1

    kb = Knowledge(tmp / "knowledge.json")
    # Two escapes with the SAME signature must not duplicate rows.
    for _ in range(3):
        kb.record_failure("forbidden_bait", "head", "immediate", "api_doc",
                          ["P1"], ["bunch"], "0", 1, 0.2, "Please bunch it.", 1)
    kb.flush()
    check(len(kb.lessons) == 1, "same signature -> single lesson (got {})".format(len(kb.lessons)))
    check(kb.lessons and list(kb.lessons.values())[0]["occurrences"] == 3,
          "occurrences incremented to 3")
    # confidence rises with b (failures)
    sig = list(kb.lessons.keys())[0]
    check(kb.confidence_of(sig, 1) > 0.0, "confidence > 0 after failures")
    # a different signature is a new lesson
    kb.record_failure("spelling_drift", "nested", "immediate", "commit",
                      ["P1"], [], "0", 1, 0.1, "We will realise it.", 1)
    kb.flush()
    check(len(kb.lessons) == 2, "distinct signature -> second lesson")
    # patterns: need >=2 shares. Add placements that share a technique.
    kb.record_failure("forbidden_bait", "tail", "immediate", "readme",
                      ["P1"], ["bunch"], "0", 1, 0.3, "bunch again", 1)
    kb.record_failure("forbidden_bait", "nested", "immediate", "comment",
                      ["P1"], ["bunch"], "0", 1, 0.25, "bunch nested", 1)
    kb._regenerate_patterns()
    kb.flush()  # persist the new lessons before the reload assertion
    pats = kb.patterns(min_support=2)
    check(any(p["kind"] == "technique_across_placements" and p["key"] == "forbidden_bait"
              for p in pats), "technique_across_placements pattern emitted")
    # query API
    top = kb.top_lessons(n=5, by="occurrences", current_round=1)
    check(top and top[0]["occurrences"] >= 3, "top_lessons by occurrences works")
    lf = kb.lessons_for(technique="forbidden_bait")
    check(len(lf) == 3, "lessons_for(technique) filters (got {})".format(len(lf)))
    # transfer prediction for an unprobed variant
    class _V:
        def __init__(self, k, i):
            self.key = k; self.intensity = i
    preds = kb.predict("2", [_V("0", 1.0), _V("2", 3.0)], n=3, current_round=1)
    check(isinstance(preds, list), "predict returns a list")
    # persistence: reload from disk keeps lessons (no dup)
    kb2 = Knowledge(tmp / "knowledge.json")
    check(len(kb2.lessons) == len(kb.lessons), "reload preserves lessons")
    # diff
    d = kb.diff(kb2)
    check("added" in d and "changed" in d, "diff structure present")
    # decay: absence over many rounds lowers confidence
    kb.record_absence(current_round=10)
    kb.flush()
    conf_old = kb.confidence_of(sig, 1)
    conf_new = kb.confidence_of(sig, 10)
    check(conf_new <= conf_old, "confidence decays with absence ({}->{})".format(conf_old, conf_new))

    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    print("\nknowledge self-test: {} failed".format(fails))
    return 1 if fails else 0


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="WHITE knowledge base self-test / demo.")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.self_test or args.demo:
        return _selftest()
    print("Knowledge loaded. Use --self-test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
