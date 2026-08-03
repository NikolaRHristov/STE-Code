#!/usr/bin/env python3
"""Unit tests for ``core.analysis`` — the jail's argument parser.

``test_jail.py`` is an end-to-end suite: it drives the group plugin and asserts
ALLOW/ESCAPE outcomes under each policy. That proves the jail behaves, but it
cannot say *which* parsing rule produced a verdict, so a rule that is right for
the wrong reason still passes.

This suite tests the parser directly, one behaviour per assertion:

    write_targets           the public tool-argument entry point
    analyze_command         shell command analysis with cwd threading
    resolve_against         relative/absolute/``~``/``$VAR`` resolution
    is_passthrough_device   the character-device allow-list
    containment_violations  the skill_manage structural invariant

Zero third-party imports. Run either way::

    python3 .agents/hermes/jail/tests/test_analysis.py
    pytest  .agents/hermes/jail/tests/test_analysis.py

Exit 0 = every case behaved as specified.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Callable, Dict, List, Tuple

_TESTS_DIR = Path(__file__).resolve().parent
_JAIL_ROOT = _TESTS_DIR.parent
if str(_JAIL_ROOT) not in sys.path:
    sys.path.insert(0, str(_JAIL_ROOT))

from core.analysis import (  # noqa: E402
    analyze_command,
    command_basenames,
    containment_violations,
    expand,
    is_passthrough_device,
    resolve_against,
    write_targets,
)

# A stable, real base directory. Using the repo root keeps ``realpath`` stable
# on macOS, where /tmp is a symlink to /private/tmp and would make raw string
# comparisons depend on the platform.
BASE = str(_JAIL_ROOT.parents[2])  # <repo>
PARENT = os.path.dirname(BASE)
HOME = os.path.realpath(os.path.expanduser("~"))


# --------------------------------------------------------------------------- #
# Tiny assertion harness (no pytest required)
# --------------------------------------------------------------------------- #
_FAILURES: List[str] = []
_CHECKS = 0


def check(condition: bool, message: str) -> None:
    global _CHECKS
    _CHECKS += 1
    if not condition:
        _FAILURES.append(message)


def paths(command: str, cwd: str = BASE) -> List[str]:
    """Resolved write targets of *command*."""
    return [p for _, p in analyze_command(command, cwd)]


def writes_to(command: str, suffix: str, cwd: str = BASE) -> bool:
    """True when some write target of *command* ends with *suffix*."""
    return any(p == suffix or p.endswith(suffix) for p in paths(command, cwd))


def has_no_targets(command: str, cwd: str = BASE) -> bool:
    """True when the command is analysed as a pure read.

    Character devices are not filesystem writes, so they do not count as
    targets for this purpose — the plugin skips them via
    ``is_passthrough_device``.
    """
    return [p for p in paths(command, cwd) if not is_passthrough_device(p)] == []


# --------------------------------------------------------------------------- #
# resolve_against / expand
# --------------------------------------------------------------------------- #
def test_resolve_against() -> None:
    check(
        resolve_against("sub/file.md", BASE) == os.path.join(BASE, "sub/file.md"),
        "relative path must anchor at the base",
    )
    check(
        resolve_against("/etc/hosts", BASE) == os.path.realpath("/etc/hosts"),
        "absolute path must ignore the base",
    )
    check(
        resolve_against("../sibling.md", BASE)
        == os.path.join(PARENT, "sibling.md"),
        "..-relative path must climb out of the base",
    )
    check(
        resolve_against("~/x.md", BASE) == os.path.join(HOME, "x.md"),
        "~ must expand to the user home",
    )
    os.environ["STE_TEST_VAR"] = "/etc"
    check(
        resolve_against("$STE_TEST_VAR/hosts", BASE) == os.path.realpath("/etc/hosts"),
        "$VAR must expand",
    )
    check(
        resolve_against("${STE_TEST_VAR}/hosts", BASE)
        == os.path.realpath("/etc/hosts"),
        "${VAR} must expand",
    )
    del os.environ["STE_TEST_VAR"]
    check(expand("~") == os.path.expanduser("~"), "expand handles a bare tilde")
    # An unset variable must not crash and must not silently become the base.
    os.environ.pop("STE_DEFINITELY_UNSET", None)
    check(
        isinstance(resolve_against("$STE_DEFINITELY_UNSET/x", BASE), str),
        "an unset variable must resolve without raising",
    )


# --------------------------------------------------------------------------- #
# is_passthrough_device
# --------------------------------------------------------------------------- #
def test_passthrough_devices() -> None:
    for device in (
        "/dev/null",
        "/dev/zero",
        "/dev/tty",
        "/dev/stdout",
        "/dev/stderr",
        "/dev/stdin",
        "/dev/console",
        "/dev/random",
        "/dev/urandom",
        "/dev/fd/1",
        "/dev/fd/255",
        "/dev/ttys003",
        "/dev/pts/0",
    ):
        check(is_passthrough_device(device), f"{device} must be a passthrough device")

    # The match is EXACT, never a prefix: a /dev/ subpath must stay gated or the
    # allow-list re-opens the hole it was carved out of.
    for device in (
        "/dev/rdisk1",
        "/dev/disk0s1",
        "/dev/nullx",
        "/dev/fd/1/../../etc/passwd",
        "/dev/../etc/passwd",
        "/dev",
        "/devnull",
        "",
    ):
        check(
            not is_passthrough_device(device),
            f"{device!r} must NOT be treated as a passthrough device",
        )


# --------------------------------------------------------------------------- #
# The `-o` regression (commit a323fa3)
# --------------------------------------------------------------------------- #
def test_dash_o_is_read_only_for_most_commands() -> None:
    """`-o` is a FORMAT/owner/overwrite flag for these — never a write target.

    Treating `-o` as a universal output flag blocked `ps -o pid=` in a live
    session. Each of these must analyse to no write target from the `-o`.
    """
    for command in (
        "ps -o pid=,command= -p 1",
        "ps -o ppid=",
        "ps -eo pid,comm",
        "git -o foo status",
        "rsync -o --dry-run src/ dst/",
        "unzip -o -l /tmp/x.zip",
        "lsof -o -p 1",
        "df -o",
    ):
        targets = [
            p for _, p in analyze_command(command, BASE) if not is_passthrough_device(p)
        ]
        # rsync/unzip may legitimately report their own operands; what must NOT
        # appear is a target derived from the `-o` flag's following token.
        check(
            not any(t.endswith("/pid=,command=") or t.endswith("/foo") for t in targets),
            f"`-o` must not name a write target in: {command}",
        )


def test_dash_o_is_a_write_flag_for_output_commands() -> None:
    """Scoping `-o` must NOT weaken the commands that really write through it."""
    check(writes_to("sort -o ../out.txt in.txt", "/out.txt"), "sort -o writes")
    check(
        writes_to("curl -o ../leak.html https://example.test", "/leak.html"),
        "curl -o writes",
    )
    check(
        writes_to("wget -O ../leak.html https://example.test", "/leak.html"),
        "wget -O writes",
    )
    check(writes_to("gcc -o ../bin/evil src.c", "/bin/evil"), "gcc -o writes")
    check(writes_to("clang -o ../a.out a.c", "/a.out"), "clang -o writes")
    check(writes_to("ld -o ../linked.o a.o", "/linked.o"), "ld -o writes")
    # The long form is universal and must work for any command.
    check(
        writes_to("somecmd --output ../generic.txt", "/generic.txt"),
        "--output is a universal write flag",
    )
    check(
        writes_to("somecmd --output=../attached.txt", "/attached.txt"),
        "--output=VALUE (attached form) is a write flag",
    )


# --------------------------------------------------------------------------- #
# Redirections
# --------------------------------------------------------------------------- #
def test_redirect_forms() -> None:
    for command, suffix in (
        ("echo x > ../a.txt", "/a.txt"),
        ("echo x >> ../b.txt", "/b.txt"),
        ("cmd 2> ../c.log", "/c.log"),
        ("cmd &> ../d.log", "/d.log"),
        ("cmd 1>> ../e.log", "/e.log"),
        ("cmd 2>> ../f.log", "/f.log"),
        ("cmd >| ../g.txt", "/g.txt"),
        ("echo x >../attached.txt", "/attached.txt"),
        ("cmd 2>../attached.log", "/attached.log"),
        ("> ../leading.txt cat in.txt", "/leading.txt"),
    ):
        check(writes_to(command, suffix), f"redirect not detected: {command}")

    # `2>&1` duplicates a descriptor; it is not a path.
    check(
        has_no_targets("diff a b > /dev/null 2>&1"),
        "fd duplication plus /dev/null is not a filesystem write",
    )
    check(
        has_no_targets("find . -name '*.py' 2>/dev/null"),
        "2>/dev/null must not be gated",
    )


# --------------------------------------------------------------------------- #
# cwd threading, subshells, grouping
# --------------------------------------------------------------------------- #
def test_cwd_threading() -> None:
    check(
        writes_to("cd .. && mkdir -p escape", os.path.join(PARENT, "escape")),
        "cd .. must move the cwd for the following segment",
    )
    check(
        writes_to("(cd /etc && mkdir -p sub)", "/etc/sub"),
        "a subshell's cd must still be followed",
    )
    check(
        writes_to("{ cd .. ; touch here.txt ; }", os.path.join(PARENT, "here.txt")),
        "brace grouping must not hide the command word",
    )
    check(
        writes_to("cd .. ; cd .. ; mkdir deep", os.path.dirname(PARENT) + "/deep"),
        "consecutive cd segments must compose",
    )
    # A bare `cd` goes home.
    check(
        writes_to("cd && touch tilde.txt", os.path.join(HOME, "tilde.txt")),
        "a bare cd must move to the user home",
    )
    # `cd` itself is a move, not a write.
    check(has_no_targets("cd .."), "cd alone writes nothing")


def test_workdir_argument() -> None:
    targets = [
        p for _, p in write_targets("terminal", {"command": "mkdir -p sub", "workdir": PARENT}, BASE)
    ]
    check(
        os.path.join(PARENT, "sub") in targets,
        "a relative mkdir must resolve against the workdir, not the base",
    )
    check(
        PARENT in targets,
        "the workdir itself must be reported as a target",
    )


# --------------------------------------------------------------------------- #
# Wrapper prefixes
# --------------------------------------------------------------------------- #
def test_wrapper_prefixes() -> None:
    for command in (
        "sudo mkdir -p ../w1",
        "doas mkdir -p ../w1",
        "nice -n 5 mkdir -p ../w1",
        "ionice -c 3 mkdir -p ../w1",
        "nohup mkdir -p ../w1",
        "setsid mkdir -p ../w1",
        "command mkdir -p ../w1",
        "exec mkdir -p ../w1",
        "time mkdir -p ../w1",
        "timeout 5 mkdir -p ../w1",
        "timeout -s KILL 5 mkdir -p ../w1",
        "stdbuf -o0 mkdir -p ../w1",
        "env mkdir -p ../w1",
        "env FOO=bar mkdir -p ../w1",
        "FOO=bar mkdir -p ../w1",
        "FOO=bar BAZ=qux mkdir -p ../w1",
        "xargs -I{} mkdir -p ../w1",
        "watch -n 1 mkdir -p ../w1",
        "sudo nice -n 5 mkdir -p ../w1",
    ):
        check(
            writes_to(command, os.path.join(PARENT, "w1")),
            f"wrapper prefix hid the real command: {command}",
        )

    # `stdbuf -o0` uses -o as its OWN flag; it must not be read as an output
    # path, and the wrapped command must still be analysed.
    check(
        not writes_to("stdbuf -o0 ls", "/0"),
        "stdbuf -o0 must not be read as an output file",
    )


# --------------------------------------------------------------------------- #
# Write commands and their operand positions
# --------------------------------------------------------------------------- #
def test_write_command_operands() -> None:
    # "all" operands
    for command in ("mkdir ../m", "touch ../m", "rm ../m", "rmdir ../m", "chmod 755 ../m"):
        check(writes_to(command, os.path.join(PARENT, "m")), f"all-operand write missed: {command}")

    # "last" operand only (cp/mv/install semantics)
    cp_targets = paths("cp a.txt b.txt ../dest/")
    check(
        any(t.startswith(PARENT) for t in cp_targets),
        "cp must report its destination",
    )
    check(
        not any(t.endswith("/a.txt") for t in cp_targets),
        "cp must NOT report its sources as writes",
    )
    check(writes_to("mv notes.md ..", PARENT), "mv into the parent is a write")
    check(writes_to("ln -s /etc/passwd ../link", "/link"), "ln -s destination is a write")
    check(writes_to("install -m 755 bin ../out/bin", "/out/bin"), "install writes its last operand")

    # Bare (non-path-like) operands still resolve under the cwd.
    check(
        writes_to("mkdir escape", os.path.join(BASE, "escape")),
        "a bare operand must resolve under the cwd",
    )

    # URLs are not filesystem paths.
    check(
        not any("://" in t for t in paths("curl https://example.test/x")),
        "a URL operand must not become a write target",
    )


def test_in_place_editors() -> None:
    check(
        writes_to("sed -i '' 's/a/b/' ../out.md", "/out.md"),
        "sed -i is a write",
    )
    check(
        writes_to("perl -i -pe s/a/b/ ../out.md", "/out.md"),
        "perl -i is a write",
    )
    check(
        has_no_targets("sed 's/a/b/' ../out.md"),
        "sed without -i is a pure read",
    )
    check(
        has_no_targets("awk '{print}' ../out.md"),
        "awk without -i is a pure read",
    )


def test_git_subcommands() -> None:
    check(writes_to("git -C .. init escaped", PARENT), "git -C is a directory flag")
    check(
        writes_to("git init ../newrepo", "/newrepo"),
        "git init names a write target",
    )
    check(
        writes_to("git clone https://x.test/r ../cloned", "/cloned"),
        "git clone names a write target",
    )
    check(
        has_no_targets("git status"),
        "git status writes to no path the analyser can name",
    )
    check(has_no_targets("git log --oneline"), "git log is a read")


def test_dd_and_tee() -> None:
    check(writes_to("dd if=/dev/zero of=../wipe.img", "/wipe.img"), "dd of= is a write")
    check(
        writes_to(f"dd if=x of={PARENT}/abs.img", "/abs.img"),
        "dd of= with an absolute path is a write",
    )
    check(
        not writes_to("dd if=../src.img of=/dev/null", "/src.img"),
        "dd if= (the SOURCE) is a read, not a write",
    )
    check(writes_to("cat f | tee ../out.log", "/out.log"), "tee names a write target")
    check(
        has_no_targets("cat f | tee /dev/stderr"),
        "tee to a character device is not a filesystem write",
    )


# --------------------------------------------------------------------------- #
# Archives — mode dependent
# --------------------------------------------------------------------------- #
def test_archive_modes() -> None:
    # LIST modes are pure reads.
    for command in (
        "tar -tzf x.tar.gz",
        "tar -tf ../outside.tar",
        "tar --list -f ../outside.tar",
        "unzip -l /tmp/x.zip",
        "unzip -t /tmp/x.zip",
    ):
        check(has_no_targets(command), f"archive listing must be a pure read: {command}")

    # CREATE writes the archive.
    check(writes_to("tar -czf ../a.tar.gz .", "/a.tar.gz"), "tar create (clustered -czf)")
    check(writes_to("tar -c -f ../a.tar .", "/a.tar"), "tar create (separate -c -f)")
    check(writes_to("tar czf ../a.tgz .", "/a.tgz"), "tar create (dashless flags)")
    check(writes_to("tar --create --file=../a.tar .", "/a.tar"), "tar --create --file=")
    check(writes_to("zip ../a.zip file.txt", "/a.zip"), "zip writes its archive")

    # EXTRACT writes the destination directory.
    check(writes_to("tar -xzf /tmp/p.tar.gz -C ..", PARENT), "tar extract into -C")
    check(
        writes_to("tar -xzf /tmp/p.tar.gz", BASE),
        "tar extract without -C writes the cwd",
    )
    check(writes_to("unzip /tmp/p.zip -d ../out", "/out"), "unzip -d destination")
    check(
        writes_to("unzip /tmp/p.zip", BASE),
        "unzip without -d writes the cwd",
    )
    # `tar -c` to stdout writes no file.
    check(
        has_no_targets("tar -cf - . | gzip"),
        "tar to stdout (-f -) names no file target",
    )


# --------------------------------------------------------------------------- #
# Embedded code: -c / -e / heredoc / nesting
# --------------------------------------------------------------------------- #
def test_inline_code() -> None:
    check(
        writes_to(
            f"python3 -c \"import os; os.makedirs('{PARENT}/py')\"", "/py"
        ),
        "python3 -c makedirs must be seen",
    )
    check(
        writes_to("python3 -c \"open('../w.txt','w')\"", "/w.txt"),
        "python3 -c open(...,'w') must be seen",
    )
    check(
        writes_to("node -e \"require('fs').writeFileSync('../n.txt','x')\"", "/n.txt"),
        "node -e writeFileSync must be seen",
    )
    check(
        writes_to("sh -c 'cd .. && mkdir -p nested'", os.path.join(PARENT, "nested")),
        "nested sh -c with a cd must be analysed",
    )
    check(
        writes_to(
            "bash -c \"sh -c 'cd .. && touch deep.txt'\"",
            os.path.join(PARENT, "deep.txt"),
        ),
        "doubly nested sh -c must be analysed",
    )
    # KNOWN OVER-APPROXIMATION, asserted so it stays deliberate: `open(...)`
    # is treated as a write regardless of mode, because the mode argument is
    # not statically knowable in general (`open(p, m)` with m computed). The
    # analyser errs toward reporting, which costs a false positive on an
    # inline read but never a missed write. Change this only with a mode-aware
    # parser, not by dropping `open` from the write-call set.
    check(
        writes_to("python3 -c \"print(open('../r.txt').read())\"", "/r.txt"),
        "an inline open() is conservatively reported regardless of mode",
    )
    check(
        has_no_targets("python3 -c \"print(1 + 1)\""),
        "inline code with no write call names no target",
    )


def test_heredocs() -> None:
    check(
        writes_to(
            "python3 - <<'EOF'\nimport os\nos.makedirs('../hd')\nEOF",
            os.path.join(PARENT, "hd"),
        ),
        "a quoted heredoc body must be scanned",
    )
    check(
        writes_to(
            "python3 - <<EOF\nimport os\nos.makedirs('../hd2')\nEOF",
            os.path.join(PARENT, "hd2"),
        ),
        "an unquoted heredoc body must be scanned",
    )
    check(
        writes_to(
            "cat <<-END\nimport os\nos.makedirs('../hd3')\nEND",
            os.path.join(PARENT, "hd3"),
        ),
        "a <<- heredoc body must be scanned",
    )
    check(
        has_no_targets("cat <<'EOF'\njust some text\nEOF"),
        "a heredoc with no write call is a pure read",
    )


# --------------------------------------------------------------------------- #
# write_targets — the tool-argument entry point
# --------------------------------------------------------------------------- #
def test_write_targets_tools() -> None:
    def only(tool: str, args: Dict[str, object]) -> List[str]:
        return [p for _, p in write_targets(tool, args, BASE)]

    check(
        only("write_file", {"path": "../x.md", "content": "x"})
        == [os.path.join(PARENT, "x.md")],
        "write_file(path) must be reported",
    )
    check(only("write_file", {"content": "x"}) == [], "write_file without a path")
    check(only("write_file", {"path": ""}) == [], "write_file with an empty path")
    check(only("write_file", {"path": 42}) == [], "write_file with a non-string path")

    check(
        only("patch", {"mode": "replace", "path": "../p.md"})
        == [os.path.join(PARENT, "p.md")],
        "patch replace mode reports its path",
    )
    check(
        only("patch", {"path": "../p.md"}) == [os.path.join(PARENT, "p.md")],
        "patch defaults to replace mode",
    )
    patch_body = (
        "*** Begin Patch\n"
        "*** Add File: ../added.py\n+print(1)\n"
        "*** Update File: ../updated.py\n+print(2)\n"
        "*** Delete File: ../deleted.py\n"
        "*** End Patch"
    )
    v4a = only("patch", {"mode": "patch", "patch": patch_body})
    for name in ("added.py", "updated.py", "deleted.py"):
        check(
            os.path.join(PARENT, name) in v4a,
            f"V4A patch must report {name}",
        )

    check(
        only("execute_code", {"code": "open('../ec.txt','w')"})
        == [os.path.join(PARENT, "ec.txt")],
        "execute_code path literals must be reported",
    )
    check(
        any(
            p == os.path.join(PARENT, "ect")
            for p in only(
                "execute_code",
                {"code": "from hermes_tools import terminal\nterminal('mkdir ../ect')"},
            )
        ),
        "a terminal() call inside execute_code must be analysed",
    )
    check(
        only("execute_code", {"code": "print(1 + 1)"}) == [],
        "pure computation names no write target",
    )

    # Tools with no write surface.
    for tool in ("read_file", "search_files", "web_search", "todo"):
        check(only(tool, {"path": "../x", "query": "x"}) == [], f"{tool} is not gated")


def test_write_targets_edge_cases() -> None:
    def targets(command: str) -> List[str]:
        return [p for _, p in write_targets("terminal", {"command": command}, BASE)]

    check(targets("") == [], "an empty command has no targets")
    check(targets("   ") == [], "a whitespace-only command has no targets")
    check(targets("ls") == [], "a bare read command has no targets")
    check(targets("mkdir") == [], "a write verb with no operand has no targets")
    check(targets("mkdir -p") == [], "only flags means no operand, so no targets")
    check(targets("rm -rf") == [], "rm with only flags has no targets")
    check(
        write_targets("terminal", {"command": None}, BASE) == [],
        "a non-string command must not raise",
    )
    check(
        write_targets("terminal", {}, BASE) == [],
        "a missing command must not raise",
    )
    # Quoted paths with spaces must survive tokenisation intact.
    check(
        writes_to('mkdir -p "../a dir/with spaces"', "/a dir/with spaces"),
        "a quoted path containing spaces must be preserved",
    )
    check(
        writes_to("mkdir -p '../single quoted'", "/single quoted"),
        "a single-quoted path must be preserved",
    )
    # An unbalanced quote must fall back to a naive split, not raise.
    check(
        isinstance(targets("mkdir -p '../unbalanced"), list),
        "an unbalanced quote must not raise",
    )


def test_command_basenames() -> None:
    check(command_basenames("ls -la") == ["ls"], "a single command")
    check(
        command_basenames("cat f | grep x | wc -l") == ["cat", "grep", "wc"],
        "every pipeline stage is reported",
    )
    check(
        "curl" in command_basenames("sh -c 'curl https://x.test'"),
        "a command hidden in sh -c must be reported",
    )
    check(
        "pip" in command_basenames("bash -c \"sh -c 'pip install x'\""),
        "a doubly nested command must be reported",
    )
    check(
        "/usr/bin/curl" not in command_basenames("/usr/bin/curl x"),
        "the basename, not the full path, is reported",
    )
    check("curl" in command_basenames("/usr/bin/curl x"), "an absolute path resolves")
    check(command_basenames("") == [], "an empty command has no basenames")


# --------------------------------------------------------------------------- #
# containment_violations
# --------------------------------------------------------------------------- #
def test_containment_violations() -> None:
    def violations(args: Dict[str, object]) -> List[Tuple[str, str]]:
        return containment_violations("skill_manage", args, BASE)

    check(
        violations({"name": "s", "file_path": "../../../escape.md"}) != [],
        "a skill traversal out of the skills tree is a containment violation",
    )
    check(
        violations({"name": "s", "file_path": "/etc/passwd"}) != [],
        "an absolute skill file_path escapes the skill directory",
    )
    check(
        violations({"name": "s", "file_path": "references/api.md"}) == [],
        "a legitimate skill support file is not a violation",
    )
    check(
        violations({"name": "s", "file_path": "scripts/deep/nested/x.py"}) == [],
        "a nested legitimate path is not a violation",
    )
    check(violations({"name": "s"}) == [], "no file_path means no violation")
    check(violations({}) == [], "empty args means no violation")
    check(
        containment_violations("write_file", {"path": "../x"}, BASE) == [],
        "containment is a skill_manage-only invariant",
    )


# --------------------------------------------------------------------------- #
# Robustness: the analyser must never raise
# --------------------------------------------------------------------------- #
def test_never_raises() -> None:
    hostile = [
        "",
        " ",
        "\n\n\n",
        ";;;;",
        "&&&&",
        "|||",
        "( ( ( (",
        ") ) ) )",
        "'",
        '"',
        "mkdir '",
        'echo "unterminated',
        ">",
        ">>",
        "> >",
        "2>",
        "cmd >",
        "cd",
        "cd " + "../" * 80,
        "mkdir " + "a/" * 500,
        "sh -c " + "'sh -c '" * 20,
        "python3 -c",
        "tar",
        "unzip",
        "zip",
        "dd of=",
        "env",
        "sudo",
        "xargs -I",
        "\x00\x01\x02",
        "mkdir $UNSET_VAR_XYZ/../../x",
        "cat <<EOF",
        "cat <<'EOF'\nno terminator",
        "a" * 5000,
    ]
    for command in hostile:
        try:
            analyze_command(command, BASE)
            write_targets("terminal", {"command": command}, BASE)
            command_basenames(command)
        except Exception as exc:  # noqa: BLE001
            _FAILURES.append(f"analyser raised on {command!r}: {exc!r}")
        _CHECKS_BUMP()


def _CHECKS_BUMP() -> None:
    global _CHECKS
    _CHECKS += 1


def test_targets_are_absolute_and_real() -> None:
    """Every reported target must be an absolute, normalised path.

    The policy compares targets against write roots by prefix. A relative or
    unnormalised target would silently fail every containment comparison.
    """
    for command in (
        "mkdir sub",
        "mkdir ../up",
        "cd .. && touch x",
        "echo x > ~/y.txt",
        "cp a $HOME/b",
        "tar -xzf p.tgz -C ../out",
        "dd if=x of=./rel.img",
    ):
        for target in paths(command):
            check(
                os.path.isabs(target),
                f"target {target!r} from {command!r} is not absolute",
            )
            check(
                ".." not in target.split(os.sep),
                f"target {target!r} from {command!r} is not normalised",
            )


def test_realpath_symlink_resolution() -> None:
    """A symlinked directory must resolve to its real location.

    Otherwise ``<repo>/link-to-parent/x`` would compare as inside the repo.
    """
    with tempfile.TemporaryDirectory() as tmp:
        real = os.path.join(tmp, "real")
        os.makedirs(real)
        link = os.path.join(tmp, "link")
        os.symlink(real, link)
        resolved = resolve_against("x.txt", link)
        check(
            resolved == os.path.join(os.path.realpath(real), "x.txt"),
            "a symlinked base must resolve to its real path",
        )


# --------------------------------------------------------------------------- #
# Runner
# --------------------------------------------------------------------------- #
TESTS: List[Callable[[], None]] = [
    test_resolve_against,
    test_passthrough_devices,
    test_dash_o_is_read_only_for_most_commands,
    test_dash_o_is_a_write_flag_for_output_commands,
    test_redirect_forms,
    test_cwd_threading,
    test_workdir_argument,
    test_wrapper_prefixes,
    test_write_command_operands,
    test_in_place_editors,
    test_git_subcommands,
    test_dd_and_tee,
    test_archive_modes,
    test_inline_code,
    test_heredocs,
    test_write_targets_tools,
    test_write_targets_edge_cases,
    test_command_basenames,
    test_containment_violations,
    test_never_raises,
    test_targets_are_absolute_and_real,
    test_realpath_symlink_resolution,
]


def main() -> int:
    print("=" * 66)
    print("core.analysis unit suite")
    print("=" * 66)
    failed_tests = 0
    for test in TESTS:
        before = len(_FAILURES)
        try:
            test()
        except Exception as exc:  # noqa: BLE001
            _FAILURES.append(f"{test.__name__} raised: {exc!r}")
        new = len(_FAILURES) - before
        status = "ok  " if new == 0 else "FAIL"
        if new:
            failed_tests += 1
        print(f"  [{status}] {test.__name__}" + (f"  ({new} failed)" if new else ""))

    print("-" * 66)
    print(f"{_CHECKS} assertions, {len(_FAILURES)} failed, {failed_tests} failing test(s)")
    if _FAILURES:
        print("\nFailures:")
        for failure in _FAILURES:
            print(f"  - {failure}")
        return 1
    print("RESULT: all assertions passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
