# Per-purpose configuration — `ste_config.py`

Path in repo: `.agents/tools/lib/ste_config.py` (symlinked into profiles).

## Public API

```python
from ste_config import load          # or: load(__file__)

cfg = load(__file__)                 # finds <unit>/config.yaml beside the script

cfg.model                            # str, from agent.model (inherited or override)
cfg.get("thresholds.total_workers") # any value; raise if missing unless default given
cfg.path("inputs.extracted")         # Path, resolved to repo root + ensure_inside_repo()
cfg.paths("outputs")                 # {name: Path} for a whole mapping section
cfg.regex("layout.worker_re")        # re.Pattern from a declared string
cfg.pattern("layout.refined_file")   # str
cfg.render("layout.refined_file", worker=7, start=1, end=4)  # -> "r007-p1-4.md"
cfg.footprint()                      # human-readable summary of inputs/outputs/agent
load(__file__, overrides={"agent.model": "x"})  # explicit arg wins over everything
load(__file__, use_env=True)         # STE_MODEL / STE_AGENT / STE_TIMEOUT override file
```

## Shared defaults without a global config

`.agents/config/defaults.yaml` may carry ONLY the `agent:` section. The loader
raises `ConfigError` if any other top-level key appears — this is the structural
guard that prevents shared defaults from silently becoming the global config the
user rejected.

```yaml
# .agents/config/defaults.yaml
agent:
    model: tencent/hy3:free
    name: hermes
    timeout_s: 600
    workers_per_batch: 3
    retries: 3
    backoff_s: 5
```

## Resolution order (lowest → highest priority)

1. `defaults.yaml` (`agent:` only)
2. `<unit>/config.yaml`
3. environment overrides (`STE_MODEL`, `STE_AGENT`, `STE_TIMEOUT`) — opt-in
4. explicit `overrides={...}` call args

A unit always wins over the shared default.

## Adding a unit config

Create `<unit>/config.yaml` next to the stage's main script:

```yaml
unit: refinement
inputs:
    extracted: ste-code/extracted
outputs:
    refined: ste-code/refined
    state: .agents/state
    checkpoint: .agents/state/refine-checkpoint.json
layout:
    worker_file: "w{worker:03d}-p{start}-{end}.md"
    worker_glob: "*.md"
    worker_re: '^w(?P<worker>\d{3})-p(?P<start>\d{1,4})-(?P<end>\d{1,4})\.md$'
format:
    encoding: utf-8
    mark_open: "<mark>"
    mark_close: "</mark>"
thresholds:
    total_workers: 109
    word_ratio_min: 0.98
agent:
    model: poolside/laguna-s-2.1:free   # stage-specific override
    workers_per_batch: 3
    timeout_s: 600
```

Then in the script:

```python
from ste_config import load as _load_config
CFG = _load_config(__file__)
MODEL = CFG.model
EXTRACTED_DIR = CFG.path("inputs.extracted")
FILENAME_RE = CFG.regex("layout.worker_re")
```

## Pitfall (hit in the real refactor)

Models differ per stage. Refinement/assembly workers use `poolside/laguna-s-2.1:free`;
extraction/adapt/extend/finalize use `tencent/hy3:free`. If you convert a stage's
`os.environ.get("STE_MODEL", "poolside/...")` to `CFG.model`, set that stage's
`agent.model` to the OLD literal first — otherwise you silently change behaviour.
Verify by importing the module and asserting `m.CFG.model == "<old literal>"`.
