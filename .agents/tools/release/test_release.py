#!/usr/bin/env python3
"""Self-tests for the release tooling.

Run:  python3 .agents/tools/release/test_release.py

No network, no git writes, no LLM. The rewrite paths (`sync.apply_line_fix`,
`sync.apply_stamp_fix`) are exercised against throwaway files under
`.agents/tmp/`, never against the repository, so a failing test cannot corrupt
a real claim site.
"""

import importlib.util as ilu
import os
import re
import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
HERE = Path(__file__).resolve().parent
SANDBOX = PROJECT / ".agents/tmp/release-selftest"


def _load(name, path):
    import sys as _sys

    _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
    from templater import load_local

    return load_local(name, path)


facts = _load("rel_facts", HERE / "facts.py")
scan = _load("rel_scan", HERE / "scan.py")
sync = _load("rel_sync", HERE / "sync.py")
changelog = _load("rel_changelog", HERE / "changelog.py")

_passed = 0
_failed = 0


def check(name, cond, detail=""):
    global _passed, _failed
    if cond:
        _passed += 1
        print(f"  ok   {name}")
    else:
        _failed += 1
        print(f"  FAIL {name}  {detail}")


def sandbox(rel: str, text: str) -> Path:
    """Write a throwaway file and return its path relative to PROJECT."""
    path = SANDBOX / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- facts -----------------------------------------------------------------

f = facts.collect()

check(
    "facts: rules counted from disk",
    isinstance(f["rules"], int) and f["rules"] > 0,
    f"got {f['rules']!r}",
)
check(
    "facts: adapted rules match final rules",
    f["rules"] == f["adapted_rules"],
    f"{f['rules']} vs {f['adapted_rules']}",
)
check("facts: 9 rule sections", f["sections"] == 9)
check("facts: categories counted", f["categories"] > 0, f"got {f['categories']}")
check(
    "facts: both page counts exposed",
    f["spec_pdf_pages"] == 434 and f["spec_pages"] > 0,
    f"{f['spec_pdf_pages']} / {f['spec_pages']}",
)
check(
    "facts: core version is semver",
    bool(re.match(r"^\d+\.\d+\.\d+$", f["versions"]["core"])),
    f["versions"]["core"],
)
check(
    "facts: every track has a version",
    all(k in f["versions"] for k in ("core", "standard", "flavor")),
)
check(
    "facts: tiers measured",
    len(f["tiers"]) == f["tier_count"] and f["tier_count"] > 0,
    f"{len(f['tiers'])} vs {f['tier_count']}",
)
check(
    "facts: tier tokens are positive",
    all(t["tokens"] > 0 for t in f["tiers"]) if f["tiers"] else False,
)
check(
    "facts: benchmark tests counted",
    f["benchmark_tests"] > 0 and f["benchmark_categories"] > 0,
)

# --- registry integrity ----------------------------------------------------

reg = scan.registry()

check("registry: parses", isinstance(reg, dict))
check(
    "registry: every count claim compiles",
    all(re.compile(c["pattern"]) for c in reg["count_claims"]),
)
check(
    "registry: every count claim names a 'value' group",
    all("value" in re.compile(c["pattern"]).groupindex for c in reg["count_claims"]),
)
check(
    "registry: every count claim resolves at least one fact",
    all(
        any(scan.resolve(f, k) is not None for k in c["facts"])
        for c in reg["count_claims"]
    ),
)
check(
    "registry: stamp facts all resolve",
    all(
        scan.resolve(f, c["fact"]) is not None
        for g in ("badges", "version_stamps")
        for c in reg[g]
        if c.get("fact") and not c.get("optional")
    ),
)
check(
    "registry: sync files exist",
    all((PROJECT / p).exists() for p in reg["sync_files"]),
    str([p for p in reg["sync_files"] if not (PROJECT / p).exists()]),
)
check(
    "registry: labels have colour + description",
    all(
        re.match(r"^[0-9A-Fa-f]{6}$", x["color"]) and x["description"]
        for x in reg["labels"]
    ),
)
check(
    "registry: pipeline output is excluded from scanning",
    all(
        any(e.startswith(d) for e in reg["scan_exclude"])
        for d in ("ste-code/artifacts/", "ste-code/adapted/", "spec/")
    ),
)

# --- scanning --------------------------------------------------------------

good = sandbox(
    "clean.md", f"STE-Code has {f['rules']} rules and {f['categories']} categories.\n"
)
bad = sandbox("dirty.md", "STE-Code has 51 rules and 19 categories.\n")
ignored = sandbox(
    "ignored.md", "Legacy note: 51 rules shipped once. <!-- release-scan:ignore -->\n"
)
rels = [str(p.relative_to(PROJECT)) for p in (good, bad, ignored)]

found = scan.scan_counts(f, reg, rels)
by_file = {}
for x in found:
    by_file.setdefault(Path(x["file"]).name, []).append(x)

check(
    "scan: correct numbers produce no finding",
    "clean.md" not in by_file,
    str(by_file.get("clean.md")),
)
check(
    "scan: stale numbers are found",
    len(by_file.get("dirty.md", [])) == 2,
    str(by_file.get("dirty.md")),
)
check(
    "scan: ignore comment suppresses a finding",
    "ignored.md" not in by_file,
    str(by_file.get("ignored.md")),
)
check(
    "scan: finding reports found and expected",
    all({"found", "expected", "line", "claim"} <= set(x) for x in found),
)
check(
    "scan: default file set is the curated list",
    scan.tracked_files(reg, wide=False)
    == [p for p in reg["sync_files"] if (PROJECT / p).exists()],
)
check(
    "scan: wide set is larger than curated",
    len(scan.tracked_files(reg, wide=True)) > len(scan.tracked_files(reg, wide=False)),
)

# --- rewriting (the write path) --------------------------------------------

pattern = next(c["pattern"] for c in reg["count_claims"] if c["id"] == "rules-count")
target = sandbox(
    "rewrite.md", "The standard defines 51 rules today.\nUnrelated: 51 apples.\n"
)
rel = str(target.relative_to(PROJECT))

ok = sync.apply_line_fix(rel, 1, "51", "54", pattern)
after = target.read_text(encoding="utf-8")
check("sync: line rewrite reports success", ok)
check("sync: number is replaced", "54 rules" in after, after)
check(
    "sync: prose around it survives", after.startswith("The standard defines "), after
)
check("sync: other lines untouched", "51 apples" in after, after)

multi = sandbox("multi.md", "Both 51 rules and 51 rules on one line.\n")
sync.apply_line_fix(str(multi.relative_to(PROJECT)), 1, "51", "54", pattern)
check(
    "sync: every match on the line is fixed",
    multi.read_text(encoding="utf-8").count("54 rules") == 2,
)

miss = sandbox("miss.md", "Nothing to fix here.\n")
check(
    "sync: no match reports failure",
    sync.apply_line_fix(str(miss.relative_to(PROJECT)), 1, "51", "54", pattern)
    is False,
)
check(
    "sync: out-of-range line reports failure",
    sync.apply_line_fix(str(miss.relative_to(PROJECT)), 99, "51", "54", pattern)
    is False,
)

stamp = sandbox("stamp.cff", 'title: "x"\nversion: 0.9.0\nlicense: MIT\n')
ok = sync.apply_stamp_fix(
    str(stamp.relative_to(PROJECT)), r"^version: (?P<value>[\d.]+)$", "1.1.0"
)
stamp_after = stamp.read_text(encoding="utf-8")
check("sync: stamp rewrite reports success", ok)
check("sync: stamp value replaced", "version: 1.1.0" in stamp_after, stamp_after)
check(
    "sync: neighbouring keys survive",
    'title: "x"' in stamp_after and "license: MIT" in stamp_after,
)

badge = sandbox(
    "badge.md",
    "[![Standard](https://img.shields.io/badge/standard-51%20rules-green)](x)\n",
)
sync.apply_stamp_fix(
    str(badge.relative_to(PROJECT)), r"badge/standard-(?P<value>\d+)%20rules-", "54"
)
check(
    "sync: badge number replaced",
    "standard-54%20rules-" in badge.read_text(encoding="utf-8"),
)

# Idempotence: a second pass must be a no-op.
before = target.read_text(encoding="utf-8")
sync.apply_line_fix(rel, 1, "51", "54", pattern)
check("sync: re-running changes nothing", target.read_text(encoding="utf-8") == before)

# --- changelog -------------------------------------------------------------

tags = changelog.core_tags()
check("changelog: core tags discovered", len(tags) > 0, str(tags))
check("changelog: tags sorted oldest first", tags == sorted(tags))

text = changelog.build(None)
check("changelog: has a title", text.startswith("# Changelog"))
check("changelog: has an Unreleased section", "## [Unreleased]" in text)
check(
    "changelog: includes every released tag",
    all(f"## [{t.lstrip('v')}]" in text for _, t in tags),
)
check("changelog: noise commits are filtered", "poll-commit" not in text)
check("changelog: bullets link to commits", "/commit/" in text)

promoted = changelog.build("1.1.0")
check("changelog: --next promotes the version", "## [1.1.0]" in promoted)
check("changelog: promotion removes Unreleased", "## [Unreleased]" not in promoted)
check("changelog: rebuild is deterministic", changelog.build(None) == text)

parsed = changelog.CONVENTIONAL.match("feat(scope)!: thing")
check(
    "changelog: conventional parser reads type, scope, bang",
    bool(parsed)
    and parsed.group("type") == "feat"
    and parsed.group("scope") == "scope"
    and parsed.group("bang") == "!",
)
check(
    "changelog: noise pattern catches poll-commits",
    bool(changelog.NOISE.match("chore(benchmark): poll-commit 2 file(s)")),
)
check(
    "changelog: noise pattern spares real commits",
    not changelog.NOISE.match("feat(release): add sync tool"),
)

# --- version bumping -------------------------------------------------------

rel_mod = _load("rel_release", HERE / "release.py")
check("release: patch bump", rel_mod.bump("1.2.3", "patch") == "1.2.4")
check("release: minor bump resets patch", rel_mod.bump("1.2.3", "minor") == "1.3.0")
check("release: major bump resets both", rel_mod.bump("1.2.3", "major") == "2.0.0")
check(
    "release: three tracks configured",
    set(rel_mod.TRACKS) == {"core", "STANDARD", "FLAVOR"},
)
check(
    "release: tag formats differ per track",
    len({v.format(v="1.0.0") for v in rel_mod.TRACKS.values()}) == 3,
)

# Multi-session safety: staging must be path-scoped, never `git add -A`, or a
# release sweeps up a concurrent session's half-written files.
src = (HERE / "release.py").read_text(encoding="utf-8")
check("release: never stages the whole tree", '"add", "-A"' not in src)
check(
    "release: owned paths exclude other sessions' dirs",
    not any(
        p.startswith(
            (
                ".agents/benchmark",
                ".agents/state",
                "ste-code/refined",
                "ste-code/grouped",
                "ste-code/extracted",
            )
        )
        for p in rel_mod.OWNED_PATHS
    ),
    str(rel_mod.OWNED_PATHS),
)
check("release: CHANGELOG.md is an owned path", "CHANGELOG.md" in rel_mod.OWNED_PATHS)
check(
    "registry: no claim site outside the owned paths",
    all(
        any(
            c["file"] == p or c["file"].startswith(p + "/") for p in rel_mod.OWNED_PATHS
        )
        for g in ("badges", "version_stamps")
        for c in reg[g]
    ),
    str(
        [
            c["file"]
            for g in ("badges", "version_stamps")
            for c in reg[g]
            if not any(
                c["file"] == p or c["file"].startswith(p + "/")
                for p in rel_mod.OWNED_PATHS
            )
        ]
    ),
)
# Ordering: sync runs before tagging, so facts must accept the version being
# released rather than reading the (not yet created) tag.
os.environ["STE_RELEASE_VERSION"] = "9.9.9"
os.environ["STE_RELEASE_DATE"] = "2099-01-01"
forced = facts.collect()
check(
    "facts: release version override applies to every track",
    all(v == "9.9.9" for v in forced["versions"].values()),
    str(forced["versions"]),
)
check("facts: release date override applies", forced["release_date"] == "2099-01-01")
del os.environ["STE_RELEASE_VERSION"], os.environ["STE_RELEASE_DATE"]
check("facts: overrides are not sticky", facts.collect()["versions"]["core"] != "9.9.9")
# Regression: CHANGELOG.md is created by step 4, so the staging list must be
# resolved AFTER it exists, not reused from the preflight snapshot.
commit_step = src.split('print("\\n6. commit")')[1].split('print("\\n7. tag")')[0]
check(
    "release: staging list is recomputed at commit time",
    "OWNED_PATHS" in commit_step and ".exists()" in commit_step,
    commit_step.strip()[:160],
)

# --- teardown --------------------------------------------------------------

for p in sorted(SANDBOX.rglob("*"), reverse=True):
    p.unlink() if p.is_file() else p.rmdir()
if SANDBOX.exists():
    SANDBOX.rmdir()
check("teardown: sandbox removed", not SANDBOX.exists())

print(f"\n{_passed} passed, {_failed} failed")
sys.exit(1 if _failed else 0)
