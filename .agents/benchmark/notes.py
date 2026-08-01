#!/usr/bin/env python3
"""Inter-colour correspondence bus. Implements NOTES_PROTOCOL.md.

The colours are independent processes: they cannot pass objects, share memory,
or await each other's return values. But they have things to tell each other,
and those things must survive the process that observed them.

A note is a durable, addressed, evidence-bearing message on disk. Three
properties make it useful rather than chatter:

  Immutable    a note is never edited after it is written. A correction is a
               new note that supersedes the old one by id, so the record of
               what was believed *at the time* is never rewritten.
  Evidenced    a claim, warning or rebuttal must cite artifact ids. A reader
               can verify the assertion instead of trusting the sender.
  Acknowledged a note that expects an answer and does not get one becomes a
               visible stale entry. Silence is reported, not lost.

Concurrency: several colours append at once. Each note is written to its own
file with an atomic temp+rename, so a reader never observes a partial note. The
index is a rebuildable cache, not the source of truth -- see IndexStore.
"""
from __future__ import annotations

import argparse
import errno
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import anonymize as _anon  # noqa: E402
from harness_config import (  # noqa: E402
    add_common_arguments, default_base, load_config, resolve_base)

SCHEMA_VERSION = 1

# Kinds that assert something about the world must cite evidence. Kinds that
# route work or answer an existing note need not: a handoff points at artifacts
# the receiver will read anyway, a request names an action rather than a fact,
# and an acknowledgement inherits the evidence of the note it answers.
EVIDENCE_REQUIRED_KINDS = ("claim", "warning", "rebuttal")
EVIDENCE_FIELDS = ("escape_ids", "probe_ids", "remedy_ids", "artifact_paths")

BROADCAST = "all"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_write(path: Path, text: str) -> None:
    """Write via temp+rename so a concurrent reader never sees a partial file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp-{}".format(os.getpid()))
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


class NoteError(RuntimeError):
    """Raised when a note violates the protocol. Never raised for I/O races."""


class Note:
    """One immutable message. Construction validates; it cannot be half-valid."""

    __slots__ = ("id", "schema_version", "from_colour", "to_colour", "variant",
                 "round", "kind", "subject", "body", "evidence", "confidence",
                 "expects_ack", "supersedes", "in_reply_to", "disposition",
                 "action_taken", "created_at")

    def __init__(self, **fields: object) -> None:
        for slot in self.__slots__:
            setattr(self, slot, fields.get(slot))
        if self.schema_version is None:
            self.schema_version = SCHEMA_VERSION
        if self.created_at is None:
            self.created_at = _utc_now()
        if self.evidence is None:
            self.evidence = {}
        if self.confidence is None:
            self.confidence = 1.0

    # ------------------------------------------------------------ validation

    def validate(self, cfg) -> "Note":
        colours = set(cfg.note_colours)
        if self.from_colour not in colours:
            raise NoteError("unknown from_colour {!r}; declared colours are {}"
                            .format(self.from_colour, sorted(colours)))
        if self.to_colour not in colours and self.to_colour != BROADCAST:
            raise NoteError("unknown to_colour {!r}; expected a colour or {!r}"
                            .format(self.to_colour, BROADCAST))
        if self.kind not in set(cfg.note_kinds):
            raise NoteError("unknown kind {!r}; declared kinds are {}"
                            .format(self.kind, sorted(cfg.note_kinds)))
        if self.disposition is not None and self.disposition not in set(cfg.ack_dispositions):
            raise NoteError("unknown disposition {!r}".format(self.disposition))
        try:
            conf = float(self.confidence)
        except (TypeError, ValueError):
            raise NoteError("confidence must be a number, got {!r}".format(self.confidence))
        if not 0.0 <= conf <= 1.0:
            raise NoteError("confidence {} outside 0..1".format(conf))
        self.confidence = conf
        if not self.subject:
            raise NoteError("a note needs a subject")
        if cfg.notes_require_evidence and self.kind in EVIDENCE_REQUIRED_KINDS:
            if not self.has_evidence():
                raise NoteError(
                    "kind {!r} asserts a fact and must cite evidence ({}); "
                    "notes are evidence, not chatter".format(
                        self.kind, ", ".join(EVIDENCE_FIELDS)))
        return self

    def has_evidence(self) -> bool:
        if not isinstance(self.evidence, dict):
            return False
        return any(self.evidence.get(field) for field in EVIDENCE_FIELDS)

    # ------------------------------------------------------------ conversion

    def to_dict(self) -> dict:
        return {slot: getattr(self, slot) for slot in self.__slots__}

    @classmethod
    def from_dict(cls, payload: dict) -> "Note":
        return cls(**payload)

    def __repr__(self) -> str:
        return "<Note {} {}->{} {} {!r}>".format(
            self.id, self.from_colour, self.to_colour, self.kind, self.subject)


class _DirLock:
    """Cross-process mutex via atomic directory creation.

    mkdir is atomic on every POSIX filesystem and, unlike an O_EXCL lock file,
    leaves nothing to clean up if the holder is killed between create and
    unlink -- a stale directory is detected by age and broken.

    Only the index needs this. Note files themselves are lock-free: each has a
    unique name and is published with an atomic rename.
    """

    def __init__(self, path: Path, timeout: float = 10.0, stale_after: float = 60.0) -> None:
        self.path = path
        self.timeout = timeout
        self.stale_after = stale_after
        self.acquired = False

    def __enter__(self) -> "_DirLock":
        deadline = time.time() + self.timeout
        while True:
            try:
                self.path.mkdir(parents=True, exist_ok=False)
                self.acquired = True
                return self
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                try:
                    age = time.time() - self.path.stat().st_mtime
                    if age > self.stale_after:
                        # The holder died. Break the lock and retry immediately.
                        self.path.rmdir()
                        continue
                except OSError:
                    pass
                if time.time() > deadline:
                    # Never block the pipeline on a lock: the index is a cache
                    # and can be rebuilt from the note files themselves.
                    return self
                time.sleep(0.01)

    def __exit__(self, *exc_info: object) -> None:
        if self.acquired:
            try:
                self.path.rmdir()
            except OSError:
                pass


class NoteBus:
    """Reads and writes notes for one results tree."""

    def __init__(self, cfg, base: "str | Path") -> None:
        self.cfg = cfg
        self.base = Path(base)
        self.dir = cfg.notes_dir(self.base)
        self.index_path = cfg.notes_index_path(self.base)
        self._lock_path = self.dir / ".index.lock"

    # ----------------------------------------------------------------- write

    def _next_seq(self, prefix: str) -> int:
        """Sequence within a (from,to,variant,round) scope.

        Derived from what is on disk rather than from a counter, so two
        processes that both write the same scope cannot hand out the same id
        from stale state -- and if they race anyway, _publish resolves it.
        """
        existing = list(self.dir.glob(prefix + "-*.json"))
        best = 0
        for path in existing:
            tail = path.stem[len(prefix) + 1:]
            if tail.isdigit():
                best = max(best, int(tail))
        return best + 1

    def write(self, from_colour: str, to_colour: str, kind: str, subject: str,
              body: str = "", variant: str = "-", round_n: int = 0,
              evidence: "dict | None" = None, confidence: float = 1.0,
              expects_ack: bool = False, supersedes: "str | None" = None,
              in_reply_to: "str | None" = None, disposition: "str | None" = None,
              action_taken: "str | None" = None) -> Note:
        note = Note(from_colour=from_colour, to_colour=to_colour, kind=kind,
                    subject=subject, body=body, variant=str(variant),
                    round=int(round_n), evidence=dict(evidence or {}),
                    confidence=confidence, expects_ack=bool(expects_ack),
                    supersedes=supersedes, in_reply_to=in_reply_to,
                    disposition=disposition, action_taken=action_taken)
        note.validate(self.cfg)
        self.dir.mkdir(parents=True, exist_ok=True)
        prefix = "{}-{}-{}-{}".format(from_colour, to_colour, note.variant, note.round)
        return self._publish(note, prefix)

    def _publish(self, note: Note, prefix: str) -> Note:
        """Claim an id and write the file, retrying if another process won."""
        for _ in range(64):
            seq = self._next_seq(prefix)
            note.id = "{}-{:03d}".format(prefix, seq)
            path = self.dir / (note.id + ".json")
            try:
                # O_EXCL is the arbiter: exactly one writer can create this id.
                fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except OSError as exc:
                if exc.errno == errno.EEXIST:
                    continue  # lost the race; take the next sequence number
                raise
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(note.to_dict(), handle, indent=2)
                handle.flush()
                os.fsync(handle.fileno())
            self._append_index(note)
            return note
        raise NoteError("could not allocate a note id under {}".format(prefix))

    def _append_index(self, note: Note) -> None:
        """Best-effort index update. The note files remain the source of truth."""
        entry = {"id": note.id, "from": note.from_colour, "to": note.to_colour,
                 "kind": note.kind, "variant": note.variant, "round": note.round,
                 "subject": note.subject, "expects_ack": note.expects_ack,
                 "in_reply_to": note.in_reply_to, "supersedes": note.supersedes,
                 "created_at": note.created_at}
        with _DirLock(self._lock_path) as lock:
            entries = self._read_index()
            entries.append(entry)
            if lock.acquired:
                _atomic_write(self.index_path, json.dumps(entries, indent=2))

    def _read_index(self) -> list:
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (OSError, ValueError):
            return []

    # ------------------------------------------------------------------ read

    def all_notes(self) -> "list[Note]":
        """Every note, read from the files themselves rather than the index.

        The index can lag if a writer was killed mid-update; the files cannot.
        Sorted by creation time so a reply always follows the note it answers.
        """
        found = []
        if not self.dir.exists():
            return found
        for path in sorted(self.dir.glob("*.json")):
            if path.name == self.cfg.handshake.notes_index:
                continue
            try:
                found.append(Note.from_dict(json.loads(path.read_text(encoding="utf-8"))))
            except (OSError, ValueError):
                continue  # a note being written right now; it will appear next scan
        found.sort(key=lambda n: (str(n.created_at), str(n.id)))
        return found

    def read(self, note_id: str) -> "Note | None":
        path = self.dir / (note_id + ".json")
        try:
            return Note.from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            return None

    def rebuild_index(self) -> int:
        """Regenerate the index from the note files. Repairs a lagging cache."""
        notes = self.all_notes()
        entries = [{"id": n.id, "from": n.from_colour, "to": n.to_colour,
                    "kind": n.kind, "variant": n.variant, "round": n.round,
                    "subject": n.subject, "expects_ack": n.expects_ack,
                    "in_reply_to": n.in_reply_to, "supersedes": n.supersedes,
                    "created_at": n.created_at} for n in notes]
        _atomic_write(self.index_path, json.dumps(entries, indent=2))
        return len(entries)

    def _filter(self, notes: "list[Note]", variant: "str | None",
                round_n: "int | None") -> "list[Note]":
        if variant is not None:
            notes = [n for n in notes if str(n.variant) == str(variant)]
        if round_n is not None:
            notes = [n for n in notes if int(n.round or 0) == int(round_n)]
        return notes

    def inbox(self, colour: str, variant: "str | None" = None,
              round_n: "int | None" = None, unacked_only: bool = False) -> "list[Note]":
        """Notes addressed to a colour, including broadcasts."""
        notes = [n for n in self.all_notes()
                 if n.to_colour == colour or n.to_colour == BROADCAST]
        notes = self._filter(notes, variant, round_n)
        notes = [n for n in notes if not self._is_superseded(n)]
        if unacked_only:
            answered = self._answered_ids()
            notes = [n for n in notes if n.expects_ack and n.id not in answered]
        return notes

    def outbox(self, colour: str, variant: "str | None" = None,
               round_n: "int | None" = None) -> "list[Note]":
        notes = [n for n in self.all_notes() if n.from_colour == colour]
        return self._filter(notes, variant, round_n)

    def _answered_ids(self) -> "set[str]":
        return {n.in_reply_to for n in self.all_notes() if n.in_reply_to}

    def _superseded_ids(self) -> "set[str]":
        return {n.supersedes for n in self.all_notes() if n.supersedes}

    def _is_superseded(self, note: Note) -> bool:
        return note.id in self._superseded_ids()

    def thread(self, note_id: str) -> "list[Note]":
        """A note plus every reply beneath it, depth-first, in time order."""
        notes = self.all_notes()
        by_parent: "dict[str, list[Note]]" = {}
        for note in notes:
            if note.in_reply_to:
                by_parent.setdefault(note.in_reply_to, []).append(note)
        root = self.read(note_id)
        if root is None:
            return []
        chain = [root]
        stack = list(by_parent.get(note_id, []))
        while stack:
            current = stack.pop(0)
            chain.append(current)
            stack = list(by_parent.get(current.id, [])) + stack
        return chain

    def acknowledge(self, note_id: str, disposition: str, action_taken: str = "",
                    rebuttal: str = "", evidence: "dict | None" = None,
                    from_colour: "str | None" = None) -> Note:
        """Answer a note. A rejection is a rebuttal and must carry evidence."""
        target = self.read(note_id)
        if target is None:
            raise NoteError("cannot acknowledge unknown note {!r}".format(note_id))
        if disposition not in set(self.cfg.ack_dispositions):
            raise NoteError("unknown disposition {!r}; expected one of {}"
                            .format(disposition, sorted(self.cfg.ack_dispositions)))
        responder = from_colour or target.to_colour
        if responder == BROADCAST:
            raise NoteError("a broadcast has no single responder; pass from_colour")
        kind = "rebuttal" if disposition == "rejected" else "acknowledgement"
        subject = "{}: {}".format(disposition, target.subject)
        return self.write(from_colour=responder, to_colour=target.from_colour,
                          kind=kind, subject=subject,
                          body=rebuttal or action_taken,
                          variant=target.variant, round_n=target.round or 0,
                          evidence=evidence, in_reply_to=target.id,
                          disposition=disposition, action_taken=action_taken)

    def stale(self, current_round: int) -> "list[Note]":
        """Notes that asked for an answer and never got one.

        Reported rather than dropped: an ignored warning is itself a finding.
        """
        answered = self._answered_ids()
        superseded = self._superseded_ids()
        horizon = int(current_round) - int(self.cfg.notes_stale_after_rounds)
        out = []
        for note in self.all_notes():
            if not note.expects_ack or note.id in answered or note.id in superseded:
                continue
            if int(note.round or 0) <= horizon:
                out.append(note)
        return out

    def summary(self) -> dict:
        """Correspondence matrix plus how reliably each colour answers."""
        notes = self.all_notes()
        answered = self._answered_ids()
        matrix: "dict[str, dict[str, int]]" = {}
        kinds: "dict[str, int]" = {}
        sent: "dict[str, int]" = {}
        expected: "dict[str, int]" = {}
        got: "dict[str, int]" = {}
        for note in notes:
            matrix.setdefault(note.from_colour, {})
            matrix[note.from_colour][note.to_colour] = \
                matrix[note.from_colour].get(note.to_colour, 0) + 1
            kinds[note.kind] = kinds.get(note.kind, 0) + 1
            sent[note.from_colour] = sent.get(note.from_colour, 0) + 1
            if note.expects_ack:
                expected[note.to_colour] = expected.get(note.to_colour, 0) + 1
                if note.id in answered:
                    got[note.to_colour] = got.get(note.to_colour, 0) + 1
        ack_rate = {}
        for colour, total in sorted(expected.items()):
            ack_rate[colour] = round(got.get(colour, 0) / total * 100, 1) if total else None
        return {"total": len(notes), "matrix": matrix, "by_kind": kinds,
                "sent": sent, "ack_expected": expected, "ack_received": got,
                "ack_rate_pct": ack_rate,
                "superseded": len(self._superseded_ids())}


# ------------------------------------------------------------------- export

def export_note(note: Note, anon) -> dict:
    """Redact one note for human consumption.

    Notes are free text written by agents plus artifact paths, which makes them
    the highest-risk leak surface in the harness. The on-disk note keeps raw
    paths so machines can resolve them; the export must not.
    """
    payload = note.to_dict()
    payload["subject"] = anon.text(str(payload.get("subject") or ""))
    payload["body"] = anon.text(str(payload.get("body") or ""))
    if payload.get("action_taken"):
        payload["action_taken"] = anon.text(str(payload["action_taken"]))
    evidence = dict(payload.get("evidence") or {})
    if evidence.get("artifact_paths"):
        evidence["artifact_paths"] = [anon.path(p) for p in evidence["artifact_paths"]]
    payload["evidence"] = evidence
    return payload


def render_markdown(notes: "list[Note]", anon, summary: "dict | None" = None) -> str:
    out: "list[str]" = ["# Correspondence", ""]
    if summary:
        out.append("{} notes · {} superseded".format(
            summary.get("total", 0), summary.get("superseded", 0)))
        rates = summary.get("ack_rate_pct") or {}
        if rates:
            out.append("Acknowledgement rate: " + ", ".join(
                "{} {}%".format(colour, pct) for colour, pct in sorted(rates.items())))
        out.append("")
        out.append("| from \\ to | " + " | ".join(sorted(
            {to for row in summary.get("matrix", {}).values() for to in row})) + " |")
        cols = sorted({to for row in summary.get("matrix", {}).values() for to in row})
        out.append("|---" * (len(cols) + 1) + "|")
        for frm in sorted(summary.get("matrix", {})):
            row = summary["matrix"][frm]
            out.append("| {} | ".format(frm) + " | ".join(
                str(row.get(col, 0)) for col in cols) + " |")
        out.append("")
    for note in notes:
        payload = export_note(note, anon)
        out.append("## {} → {} · {}".format(
            payload["from_colour"], payload["to_colour"], payload["kind"]))
        out.append("")
        out.append("**{}**".format(payload["subject"]))
        out.append("")
        if payload.get("body"):
            out.append(payload["body"])
            out.append("")
        meta = ["id `{}`".format(payload["id"]),
                "variant `{}`".format(payload["variant"]),
                "round {}".format(payload["round"]),
                "confidence {}".format(payload["confidence"])]
        if payload.get("in_reply_to"):
            meta.append("in reply to `{}`".format(payload["in_reply_to"]))
        if payload.get("supersedes"):
            meta.append("supersedes `{}`".format(payload["supersedes"]))
        if payload.get("disposition"):
            meta.append("disposition **{}**".format(payload["disposition"]))
        if payload.get("expects_ack"):
            meta.append("awaiting acknowledgement")
        out.append("<sub>" + " · ".join(meta) + "</sub>")
        cited = {k: v for k, v in (payload.get("evidence") or {}).items() if v}
        if cited:
            out.append("")
            out.append("Evidence: " + "; ".join(
                "{}={}".format(k, ", ".join(str(x) for x in v)) for k, v in sorted(cited.items())))
        out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------- CLI

def _print_notes(notes: "list[Note]", anon) -> None:
    if not notes:
        print("  (none)")
        return
    for note in notes:
        payload = export_note(note, anon)
        flag = ""
        if payload.get("expects_ack"):
            flag = " [awaiting ack]"
        if payload.get("disposition"):
            flag = " [{}]".format(payload["disposition"])
        print("  {:<34} {:>6} -> {:<6} {:<16}{}".format(
            payload["id"], payload["from_colour"], payload["to_colour"],
            payload["kind"], flag))
        print("      {}".format(payload["subject"]))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inter-colour correspondence bus (see NOTES_PROTOCOL.md).")
    cfg_preview = load_config()
    add_common_arguments(parser, config=cfg_preview)
    _anon.add_arguments(parser)
    parser.add_argument("--colour", default=None, help="colour whose mail to show")
    parser.add_argument("--inbox", action="store_true")
    parser.add_argument("--outbox", action="store_true")
    parser.add_argument("--unacked", action="store_true", help="inbox: only unanswered")
    parser.add_argument("--thread", default=None, metavar="NOTE_ID")
    parser.add_argument("--stale", type=int, default=None, metavar="CURRENT_ROUND")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--export", default=None, metavar="PATH",
                        help="write the redacted correspondence as markdown")
    parser.add_argument("--rebuild-index", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.profile)
    base = resolve_base(cfg, args.base)
    bus = NoteBus(cfg, base)
    anon = _anon.from_args(args, root=cfg.root,
                           extra_terms=[cfg.profile_id, cfg.display_name])

    if args.rebuild_index:
        print("index rebuilt: {} entries".format(bus.rebuild_index()))
        return 0

    if args.thread:
        chain = bus.thread(args.thread)
        if args.json:
            print(json.dumps([export_note(n, anon) for n in chain], indent=2))
        else:
            print("thread {} ({} notes)".format(args.thread, len(chain)))
            _print_notes(chain, anon)
        return 0

    if args.stale is not None:
        notes = bus.stale(args.stale)
        if args.json:
            print(json.dumps([export_note(n, anon) for n in notes], indent=2))
        else:
            print("stale at round {} ({} unanswered past {} rounds)".format(
                args.stale, len(notes), cfg.notes_stale_after_rounds))
            _print_notes(notes, anon)
        return 0

    if args.summary:
        summary = bus.summary()
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print("correspondence: {} notes, {} superseded".format(
                summary["total"], summary["superseded"]))
            for frm in sorted(summary["matrix"]):
                for to, count in sorted(summary["matrix"][frm].items()):
                    print("  {:>6} -> {:<6} {}".format(frm, to, count))
            for kind, count in sorted(summary["by_kind"].items()):
                print("  kind {:<16} {}".format(kind, count))
            for colour, pct in sorted((summary["ack_rate_pct"] or {}).items()):
                print("  ack rate {:<6} {}%".format(colour, pct))
        return 0

    if args.export:
        notes = bus.all_notes()
        text = render_markdown(notes, anon, bus.summary())
        out = Path(args.export)
        _atomic_write(out, text)
        print("exported {} notes to {} (anonymize={})".format(
            len(notes), anon.path(out), anon.level))
        return 0

    if args.inbox or args.outbox:
        if not args.colour:
            parser.error("--inbox/--outbox require --colour")
        notes = (bus.inbox(args.colour, unacked_only=args.unacked)
                 if args.inbox else bus.outbox(args.colour))
        if args.json:
            print(json.dumps([export_note(n, anon) for n in notes], indent=2))
        else:
            print("{} for {} ({} notes)".format(
                "inbox" if args.inbox else "outbox", args.colour, len(notes)))
            _print_notes(notes, anon)
        return 0

    notes = bus.all_notes()
    print("{} notes under {}".format(len(notes), anon.path(bus.dir)))
    _print_notes(notes, anon)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



