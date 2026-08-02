.DEFAULT_GOAL := check

PY := python3
BENCH := .agents/benchmark
JAIL := .agents/hermes/jail

# Modules held to the current style. Legacy scripts (orchestrator*, purple,
# benchmark-levels, generate_adhoc_tests) predate it and are migrated
# opportunistically -- gating on them would make `lint` permanently red and
# therefore ignored.
CLEAN := $(BENCH)/anonymize.py $(BENCH)/harness_config.py $(BENCH)/notes.py \
         $(BENCH)/purple_stitch.py $(BENCH)/verification.py $(BENCH)/black.py \
         $(BENCH)/selftest.py

## test: the canonical green check for the adversarial benchmark
test:
	@$(PY) $(BENCH)/selftest.py

## lint: syntax across the suite, style on the modules held to it
lint:
	@$(PY) -m compileall -q $(BENCH) >/dev/null && echo "compile: ok"
	@awk 'length>100 {print FILENAME":"FNR": "length" chars"; bad=1} \
		END {exit bad+0}' $(CLEAN) && echo "line length: ok"

## audit: prove emitted reports carry no operator identity
audit:
	@$(PY) $(BENCH)/anonymize.py >/dev/null && echo "anonymizer: ok"

## jail: prove the write-confinement plugins block folder escapes
jail:
	@set -o pipefail; $(PY) $(JAIL)/tests/test_jail.py | grep -E "^RESULT:"

## check: everything CI should run for the benchmark
check: lint test audit jail

# --- skill distribution -------------------------------------------------------
# Keep .agents/skills/ the single source of truth: every profile loads its
# STE skill buckets through a two-level symlink chain into that directory.
# `skills-link` asserts the links exist; `skills-check` reports drift without
# changing anything. Run `skills-prune` once to drop foreign default buckets
# that leaked into a live profile.

HERMES := .agents/hermes
SKILLS_LINK := $(HERMES)/skills-link.sh

## skills-link: symlink every STE profile's skill buckets into the single source
skills-link:
	@bash $(SKILLS_LINK) --all

## skills-check: report drift (foreign/real-copy skills) without changing files
skills-check:
	@bash $(SKILLS_LINK) --status

## skills-prune: remove foreign default skill buckets from live profiles
skills-prune:
	@bash $(SKILLS_LINK) --all --prune

# --- release maintenance -----------------------------------------------------
# Deliberately NOT wired into `check`: the benchmark suite above is another
# session's canonical gate, and mixing counts hides its real pass total.

RELEASE := .agents/tools/release

## release-test: self-tests for the release tooling
release-test:
	@$(PY) $(RELEASE)/test_release.py

## drift: documented counts, badges, and versions must match disk
drift:
	@$(PY) $(RELEASE)/scan.py

## release-check: lint + tests + drift for the release tooling only
release-check:
	@$(PY) -m compileall -q $(RELEASE) >/dev/null && echo "compile: ok"
	@awk 'length>100 {print FILENAME":"FNR": "length" chars"; bad=1} \
		END {exit bad+0}' $(RELEASE)/*.py && echo "line length: ok"
	@$(PY) $(RELEASE)/test_release.py
	@$(PY) $(RELEASE)/scan.py

.PHONY: test lint audit check release-test drift release-check \
        skills-link skills-check skills-prune
