.DEFAULT_GOAL := check

PY := python3
BENCH := .agents/benchmark
JAIL := .agents/hermes/plugins/ste-code-jail

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

## jail: prove the write-confinement plugin blocks folder escapes
jail:
	@$(PY) $(JAIL)/selftest.py >/dev/null && echo "ste-code-jail: ok"

## check: everything CI should run for the benchmark
check: lint test audit jail

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

.PHONY: test lint audit check release-test drift release-check
