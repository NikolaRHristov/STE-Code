.DEFAULT_GOAL := check

PY := python3
BENCH := .agents/benchmark
RELEASE := .agents/tools/release

# Modules held to the current style. Legacy scripts (orchestrator*, purple,
# benchmark-levels, generate_adhoc_tests) predate it and are migrated
# opportunistically -- gating on them would make `lint` permanently red and
# therefore ignored.
CLEAN := $(BENCH)/anonymize.py $(BENCH)/harness_config.py $(BENCH)/notes.py \
         $(BENCH)/purple_stitch.py $(BENCH)/selftest.py \
         $(RELEASE)/facts.py $(RELEASE)/scan.py $(RELEASE)/sync.py \
         $(RELEASE)/changelog.py $(RELEASE)/release.py $(RELEASE)/test_release.py

## test: the canonical green check
test:
	@$(PY) $(BENCH)/selftest.py
	@$(PY) $(RELEASE)/test_release.py

## lint: syntax across the suite, style on the modules held to it
lint:
	@$(PY) -m compileall -q $(BENCH) $(RELEASE) >/dev/null && echo "compile: ok"
	@awk 'length>100 {print FILENAME":"FNR": "length" chars"; bad=1} \
		END {exit bad+0}' $(CLEAN) && echo "line length: ok"

## drift: documented counts, badges, and versions must match disk
drift:
	@$(PY) $(RELEASE)/scan.py

## audit: prove emitted reports carry no operator identity
audit:
	@$(PY) $(BENCH)/anonymize.py >/dev/null && echo "anonymizer: ok"

## check: everything CI should run
check: lint test audit

.PHONY: test lint drift audit check
