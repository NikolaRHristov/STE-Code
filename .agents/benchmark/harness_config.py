#!/usr/bin/env python3
"""Generic configuration layer for the adversarial benchmark harness.

DESIGN CONTRACT
---------------
No module in this harness may hardcode:

  * a project name, standard name, or product name
  * a directory layout ("ste-code/artifacts/levelN/...")
  * a variant identifier scheme (tiers, levels, sizes, model names)
  * a vocabulary bank, technique list, placement list, or timing list
  * the name of the scoring backend

All of that is DATA, loaded from a profile document (default:
``config/harness.json`` beside this file). Retargeting the harness at a
different standard, corpus, product, or scoring backend is a config edit,
never a code edit.

The harness speaks in neutral nouns:

  variant   — one configuration under test (a prompt tier, a model, a
              policy revision; the harness does not care which)
  round     — one iteration of the adversarial loop
  runner    — whatever actually scores a batch of cases
  handshake — the filesystem contract by which independent processes converge

Usage::

    from harness_config import load_config
    cfg = load_config()                       # default profile
    cfg = load_config("/path/to/other.json")  # retargeted profile

    cfg.variant_prompt("0")        -> Path to that variant's system prompt
    cfg.round_dir(base, "0", 1)    -> Path to variant0/round1
    cfg.build_runner_argv(...)     -> argv list for the scoring backend
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

_HERE = Path(__file__).resolve().parent
DEFAULT_PROFILE = _HERE / "config" / "harness.json"
ENV_PROFILE = "BENCH_HARNESS_PROFILE"


class ConfigError(RuntimeError):
    """Raised when the profile document is missing or internally inconsistent."""


def _find_root(start: Path, markers: Sequence[str]) -> Path:
    """Walk upward from ``start`` until a directory containing a marker is found.

    Falls back to two levels above this file, which is the historical layout,
    rather than raising — a harness that cannot locate its root is still useful
    for pure generation work.
    """
    for candidate in [start, *start.parents]:
        for marker in markers:
            if (candidate / marker).exists():
                return candidate
    return _HERE.parent.parent


@dataclass(frozen=True)
class Variant:
    """One configuration under test.

    ``key`` is an opaque string. The harness never parses it, never assumes it
    is numeric, and never derives ``directory`` from it.
    """

    key: str
    directory: str
    label: str = ""
    intensity: int = 1
    extra: dict = field(default_factory=dict)

    @property
    def slug(self) -> str:
        """Filesystem-safe form of the key, for use in path components."""
        return self.key.replace("/", "-").replace(os.sep, "-")


@dataclass(frozen=True)
class Handshake:
    """Filenames that independent processes use to converge on disk.

    Every participant reads these from config. Nobody hardcodes a filename,
    so a fork of the harness can rename the whole protocol in one place.
    """

    round_dir_template: str
    red_ledger: str
    red_sentinel: str
    blue_sentinel: str
    white_sentinel: str
    black_sentinel: str
    stitch_report: str
    knowledge_base: str
    notes_dir: str
    notes_index: str
    attack_brief: str
    verdicts: str


@dataclass(frozen=True)
class Scoring:
    base: float
    principle_weight: float
    forbidden_penalty: float
    keyword_bonus: float
    pattern_penalty: float
    pass_threshold: float

    def score(
        self,
        principles_satisfied: int,
        principles_expected: int,
        forbidden_found: int,
        forbidden_total: int,
        keywords_found: int,
        keywords_total: int,
        patterns_missed: int = 0,
        patterns_total: int = 0,
    ) -> float:
        """Reference implementation of the scoring formula, clamped to [0, 1].

        Kept here so RED, BLUE, PURPLE and WHITE all agree on the arithmetic
        without importing the scoring backend.
        """

        def _ratio(num: int, den: int) -> float:
            return (num / den) if den else 0.0

        value = (
            self.base
            + self.principle_weight * _ratio(principles_satisfied, principles_expected)
            - self.forbidden_penalty * _ratio(forbidden_found, forbidden_total)
            + self.keyword_bonus * _ratio(keywords_found, keywords_total)
            - self.pattern_penalty * _ratio(patterns_missed, patterns_total)
        )
        return max(0.0, min(1.0, value))

    def passed(self, value: float) -> bool:
        return value >= self.pass_threshold


class HarnessConfig:
    """Parsed, validated view of a profile document."""

    def __init__(self, document: dict, source: Path) -> None:
        self._doc = document
        self.source = source

        paths = document.get("paths", {})
        self.root = _find_root(source.parent, paths.get("root_markers", [".git"]))

        self.profile_id = document.get("profile", {}).get("id", "harness")
        self.display_name = document.get("profile", {}).get("display_name", self.profile_id)
        self.rule_prefix = document.get("profile", {}).get("rule_prefix", "P")
        self.rule_count = int(document.get("profile", {}).get("rule_count", 0))

        self._variant_prompt_template = paths.get(
            "variant_prompt_template", "{variant_dir}/system-prompt.txt"
        )
        self.static_cases = self._resolve(paths.get("static_cases", "test-cases"))
        self.generated_cases = self._resolve(paths.get("generated_cases", "test-cases-generated"))
        self.results_base = self._resolve(paths.get("results_base", "tests"))
        self.scratch = self._resolve(paths.get("scratch", "tmp"))
        self.state = self._resolve(paths.get("state", "state"))

        runner = document.get("runner", {})
        self.runner_kind = runner.get("kind", "subprocess")
        self.runner_entrypoint = self._resolve(runner.get("entrypoint", ""))
        self._runner_argv_template = list(runner.get("argv_template", []))
        self.aggregate_filename = runner.get("aggregate_filename", "aggregate-results.json")
        self.per_test_filename = runner.get("per_test_filename", "per-test-results.json")
        self.run_dir_glob = runner.get("run_dir_glob", "run-*")
        self.default_model = runner.get("default_model", "")
        self.default_max_workers = int(runner.get("default_max_workers", 2))
        self.default_timeout_s = int(runner.get("default_timeout_s", 600))
        self.default_poll_interval_s = int(runner.get("default_poll_interval_s", 2))
        self.default_rounds = int(runner.get("default_rounds", 3))
        self.base_dir = Path(runner.get("base_dir",
                                        str(Path(self.root) / "benchmark-runs")))

        variants = document.get("variants", {})
        registry = variants.get("registry", {})
        order = variants.get("order") or sorted(registry)
        self._variants: "dict[str, Variant]" = {}
        for key in order:
            entry = registry.get(key)
            if entry is None:
                raise ConfigError(f"variant '{key}' in order[] has no registry entry")
            known = {"dir", "label", "intensity"}
            self._variants[str(key)] = Variant(
                key=str(key),
                directory=entry["dir"],
                label=entry.get("label", ""),
                intensity=int(entry.get("intensity", 1)),
                extra={k: v for k, v in entry.items() if k not in known},
            )
        self.variant_order = [str(k) for k in order]

        hs = document.get("handshake", {})
        self.handshake = Handshake(
            round_dir_template=hs.get("round_dir_template", "{base}/variant{variant}/round{round}"),
            red_ledger=hs.get("red_ledger", "escapes.json"),
            red_sentinel=hs.get("red_sentinel", "purple.json"),
            blue_sentinel=hs.get("blue_sentinel", "blue-done.json"),
            white_sentinel=hs.get("white_sentinel", "white-done.json"),
            black_sentinel=hs.get("black_sentinel", "black-done.json"),
            stitch_report=hs.get("stitch_report", "report.json"),
            knowledge_base=hs.get("knowledge_base", "knowledge.json"),
            notes_dir=hs.get("notes_dir", "notes"),
            notes_index=hs.get("notes_index", "index.json"),
            attack_brief=hs.get("attack_brief", "attack-brief.json"),
            verdicts=hs.get("verdicts", "verdicts.json"),
        )

        notes = document.get("notes", {})
        self.note_colours = list(notes.get("colours", []))
        self.note_kinds = list(notes.get("kinds", []))
        self.ack_dispositions = list(notes.get("ack_dispositions", []))
        self.notes_stale_after_rounds = int(notes.get("stale_after_rounds", 2))
        self.notes_require_evidence = bool(notes.get("require_evidence", True))

        verification = document.get("verification", {})
        self.partition_strategies = list(verification.get("partition_strategies", []))
        self.default_partition_strategy = verification.get("default_strategy", "random_half")
        self.derivation_arm = verification.get("derivation_arm", "A")
        self.verification_arm = verification.get("verification_arm", "B")
        self.overfit_tolerance_pct = float(verification.get("overfit_tolerance_pct", 10.0))
        self.min_arm_size = int(verification.get("min_arm_size", 8))
        self.verdict_kinds = list(verification.get("verdicts", []))
        self.split_seed = int(verification.get("split_seed", 7))

        sc = document.get("scoring", {})
        self.scoring = Scoring(
            base=float(sc.get("base", 0.40)),
            principle_weight=float(sc.get("principle_weight", 0.60)),
            forbidden_penalty=float(sc.get("forbidden_penalty", 0.30)),
            keyword_bonus=float(sc.get("keyword_bonus", 0.10)),
            pattern_penalty=float(sc.get("pattern_penalty", 0.20)),
            pass_threshold=float(sc.get("pass_threshold", 0.70)),
        )

        self.vocabulary = document.get("vocabulary", {})
        self.techniques = list(document.get("techniques", {}).get("enabled", []))
        self.placements = list(document.get("placements", {}).get("enabled", []))
        self.timings = list(document.get("timings", {}).get("enabled", []))

        defense = document.get("defense", {})
        self.probe_placements = list(defense.get("probe_placements", []))
        self.defense_timings = list(defense.get("timings", []))
        self.defense_window = int(defense.get("window", 2))
        self.defense_budget = int(defense.get("budget", 64))
        self.defense_threshold_pct = float(defense.get("threshold_pct", 95.0))

        limits = document.get("limits", {})
        self.max_tokens_default = int(limits.get("max_tokens_default", 1500))
        self.await_timeout_s = int(limits.get("await_timeout_s", 3600))
        self.poll_interval_s = int(limits.get("poll_interval_s", 15))

    # ---------------------------------------------------------------- paths

    def _resolve(self, value: str) -> Path:
        if not value:
            return self.root
        path = Path(value)
        return path if path.is_absolute() else (self.root / path)

    def variant(self, key: str) -> Variant:
        try:
            return self._variants[str(key)]
        except KeyError:
            known = ", ".join(self.variant_order)
            raise ConfigError(f"unknown variant '{key}'; known variants: {known}") from None

    def all_variants(self) -> "list[Variant]":
        return [self._variants[k] for k in self.variant_order]

    def variant_prompt(self, key: str) -> Path:
        variant = self.variant(key)
        rendered = self._variant_prompt_template.format(
            variant_dir=variant.directory,
            variant_key=variant.key,
            variant_slug=variant.slug,
        )
        return self._resolve(rendered)

    def parse_variants(self, spec: "str | None") -> "list[str]":
        """Turn a CLI ``--variants`` string into a validated key list.

        ``None`` or ``"all"`` selects every configured variant, in profile order.
        """
        if not spec or spec.strip().lower() == "all":
            return list(self.variant_order)
        keys = [part.strip() for part in spec.split(",") if part.strip()]
        for key in keys:
            self.variant(key)  # raises with a helpful message when unknown
        return keys

    # ------------------------------------------------------------ handshake

    def round_dir(self, base: "str | Path", variant: str, round_n: int) -> Path:
        return Path(
            self.handshake.round_dir_template.format(
                base=str(base), variant=self.variant(variant).slug, round=round_n
            )
        )

    def red_ledger_path(self, base: "str | Path", variant: str, round_n: int) -> Path:
        return self.round_dir(base, variant, round_n) / self.handshake.red_ledger

    def red_sentinel_path(self, base: "str | Path", variant: str, round_n: int) -> Path:
        return self.round_dir(base, variant, round_n) / self.handshake.red_sentinel

    def blue_sentinel_path(self, base: "str | Path", variant: str, round_n: int) -> Path:
        return self.round_dir(base, variant, round_n) / self.handshake.blue_sentinel

    def white_sentinel_path(self, base: "str | Path", variant: str, round_n: int) -> Path:
        return self.round_dir(base, variant, round_n) / self.handshake.white_sentinel

    def black_sentinel_path(self, base: "str | Path", variant: str, round_n: int) -> Path:
        return self.round_dir(base, variant, round_n) / self.handshake.black_sentinel

    def notes_dir(self, base: "str | Path") -> Path:
        """Correspondence lives at the base, not per round: notes cross rounds."""
        return Path(base) / self.handshake.notes_dir

    def notes_index_path(self, base: "str | Path") -> Path:
        return self.notes_dir(base) / self.handshake.notes_index

    def attack_brief_path(self, base: "str | Path") -> Path:
        return Path(base) / self.handshake.attack_brief

    def verdicts_path(self, base: "str | Path") -> Path:
        return Path(base) / self.handshake.verdicts

    # --------------------------------------------------------------- runner

    def build_runner_argv(
        self,
        test_dir: "str | Path",
        system_prompt: "str | Path",
        results_dir: "str | Path",
        model: "str | None" = None,
        max_workers: "int | None" = None,
        timeout: "int | None" = None,
        poll_interval: "int | None" = None,
        python: "str | None" = None,
    ) -> "list[str]":
        """Render the scoring-backend command line from the profile template.

        The harness never writes flag names inline; swapping in a different
        backend is an ``argv_template`` edit.
        """
        import sys

        values = {
            "test_dir": str(test_dir),
            "system_prompt": str(system_prompt),
            "results_dir": str(results_dir),
            "model": model or self.default_model,
            "max_workers": str(self.default_max_workers
                                if max_workers is None else max_workers),
            "timeout": str(timeout if timeout is not None else self.default_timeout_s),
            "poll_interval": str(
                poll_interval if poll_interval is not None else self.default_poll_interval_s
            ),
        }
        argv = [python or sys.executable, str(self.runner_entrypoint)]
        for token in self._runner_argv_template:
            argv.append(token.format(**values))
        return argv

    def latest_run_dir(self, results_dir: "str | Path") -> "Path | None":
        runs = sorted(Path(results_dir).glob(self.run_dir_glob))
        return runs[-1] if runs else None

    def read_run_artifacts(self, results_dir: "str | Path") -> "tuple[dict | None, list]":
        """Return ``(aggregate, per_test)`` from the most recent run directory."""
        run = self.latest_run_dir(results_dir)
        if run is None:
            return None, []
        aggregate = None
        agg_path = run / self.aggregate_filename
        if agg_path.exists():
            try:
                aggregate = json.loads(agg_path.read_text())
            except (ValueError, OSError):
                aggregate = None
        per_test: list = []
        per_path = run / self.per_test_filename
        if per_path.exists():
            try:
                per_test = json.loads(per_path.read_text())
            except (ValueError, OSError):
                per_test = []
        return aggregate, per_test

    # ----------------------------------------------------------- vocabulary

    def bank(self, name: str, default: "Iterable[Any] | None" = None) -> list:
        """Fetch a named word bank from the profile.

        Generators call ``cfg.bank("forbidden_bank")`` instead of owning a
        literal list, so a new domain ships a new profile and nothing else.
        """
        value = self.vocabulary.get(name)
        if value is None:
            if default is None:
                raise ConfigError(f"vocabulary bank '{name}' is not defined in {self.source}")
            return list(default)
        return list(value)

    def rule(self, index: int) -> str:
        """Render a rule identifier (``P4``) without hardcoding the prefix."""
        return f"{self.rule_prefix}{index}"

    def as_dict(self) -> dict:
        return dict(self._doc)


_CACHE: "dict[str, HarnessConfig]" = {}


def load_config(path: "str | Path | None" = None, *, reload: bool = False) -> HarnessConfig:
    """Load a profile document.

    Resolution order: explicit ``path`` argument, then the ``BENCH_HARNESS_PROFILE``
    environment variable, then the packaged default profile.
    """
    resolved = Path(path or os.environ.get(ENV_PROFILE) or DEFAULT_PROFILE).resolve()
    key = str(resolved)
    if not reload and key in _CACHE:
        return _CACHE[key]
    if not resolved.exists():
        raise ConfigError(f"harness profile not found: {resolved}")
    try:
        document = json.loads(resolved.read_text())
    except ValueError as exc:
        raise ConfigError(f"harness profile is not valid JSON: {resolved}: {exc}") from exc
    config = HarnessConfig(document, resolved)
    _CACHE[key] = config
    return config


def add_common_arguments(parser, *, config: "HarnessConfig | None" = None) -> None:
    """Attach the flags every harness participant shares.

    Keeps RED, BLUE, PURPLE and WHITE from drifting apart on flag names.
    """
    cfg = config or load_config()
    parser.add_argument("--profile", default=None,
                        help="path to a harness profile document (overrides the default)")
    parser.add_argument("--variants", default="all",
                        help="comma-separated variant keys, or 'all' ({})".format(
                            ",".join(cfg.variant_order)))
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--base", default=None,
                        help="results base directory (default: <results_base>/redblue)")
    parser.add_argument("--model", default=None)
    parser.add_argument("--max-workers", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=None)
    parser.add_argument("--poll-interval", type=int, default=None)
    parser.add_argument("--skip-live", action="store_true",
                        help="generate artifacts without invoking the scoring backend")


def default_base(config: HarnessConfig) -> Path:
    return config.results_base / "redblue"


if __name__ == "__main__":
    import sys

    cfg = load_config(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"profile        : {cfg.profile_id} ({cfg.display_name}) <- {cfg.source}")
    print(f"root           : {cfg.root}")
    print(f"variants       : {', '.join(cfg.variant_order)}")
    for variant in cfg.all_variants():
        prompt = cfg.variant_prompt(variant.key)
        mark = "ok " if prompt.exists() else "MISSING"
        print(f"  {variant.key:>3} {variant.directory:<9} intensity={variant.intensity} "
              f"{mark} {prompt.relative_to(cfg.root)}")
    print(f"techniques     : {len(cfg.techniques)} -> {', '.join(cfg.techniques)}")
    print(f"placements     : {len(cfg.placements)} -> {', '.join(cfg.placements)}")
    print(f"timings        : {len(cfg.timings)} -> {', '.join(cfg.timings)}")
    print(f"probe placements: {len(cfg.probe_placements)}")
    print(f"defense timings : {len(cfg.defense_timings)}")
    print(f"runner         : {cfg.runner_entrypoint.name} kind={cfg.runner_kind}")
    print(f"handshake      : ledger={cfg.handshake.red_ledger} red={cfg.handshake.red_sentinel} "
          f"blue={cfg.handshake.blue_sentinel} white={cfg.handshake.white_sentinel}")
    demo = cfg.round_dir(default_base(cfg), cfg.variant_order[0], 1)
    print(f"round dir demo : {demo}")
    print("runner argv    :", " ".join(cfg.build_runner_argv("T", "S", "R")[:6]), "...")
