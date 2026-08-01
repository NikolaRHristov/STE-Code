.DEFAULT_GOAL := check

PY := python3
BENCH := .agents/benchmark

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

## check: everything CI should run for the benchmark
check: lint test audit

.PHONY: test lint audit check
