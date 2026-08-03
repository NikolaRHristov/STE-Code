# STE-Code Agents - Benchmark & Pipeline

> **Project root:** `.agents/` **Pipeline spec:** `ste-code/` (ASD-STE100 →
> STE-Code adaptation) **Default agent:** Hermes (configured in
> `.agents/config/agents.yaml`) **Framework:** Agent-agnostic (pre-configured
> for Hermes, supports Claude, Codex, custom)

## Agent Runner

All scripts use the **agent-agnostic runner** at
`.agents/tools/lib/agent-runner.py`. Configure backends in
`.agents/config/agents.yaml`. The default model is declared there and surfaced
to every stage through `ste_config` (`CFG.model`) - it is never hardcoded in a
script.

```bash
# Use default agent (Hermes)
python3 .agents/tools/refinement/assemble-level1.py

# Use a different agent
python3 .agents/tools/refinement/assemble-level1.py --agent claude

# List available agents
python3 .agents/tools/lib/agent-runner.py --list

# Shell launcher (agent-agnostic)
.agents/tools/shared/launch-worker.sh prompt.txt --agent hermes --model poolside/laguna-s-2.1:free out.txt
```

Adding a new agent: edit `.agents/config/agents.yaml` and add your backend.

## Configuration (one source of truth)

Tunables live in config, not in code. Each `tools/<unit>/` owns a `config.yaml`
declaring its footprint; `.agents/config/defaults.yaml` supplies shared `agent:`
and `runtime:` knobs merged underneath. Stages read `ste_config.load(__file__)`
for footprint and `ste_runtime.resolve(__file__)` for pre-flight knobs (wrapper
path, retry count, batch divisor, encoding). Writes go only through `ste_io`,
confined to the repo by the jail policy.

## Quick Navigation

| Directory                    | Purpose                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------- |
| [`MASTER.md`](MASTER.md)     | Full launch protocol, terminology, pipeline stages                              |
| [`README.md`](README.md)     | Project overview                                                                |
| [`config/`](config/)         | Agent backend configuration (`agents.yaml`) + shared defaults (`defaults.yaml`) |
| [`agent/`](agent/)           | Agent role definitions (9 agents)                                               |
| [`benchmark/`](benchmark/)   | STE-Code benchmarking suite (59 tests, 14 categories)                           |
| [`prompts/`](prompts/)       | Worker prompts (adapt, enrich, OSS, refine batches)                             |
| [`skills/`](skills/)         | Agent skill definitions (extraction, refinement, adaptation, etc.)              |
| [`references/`](references/) | Shared references (rails, quality checklist, worker grid)                       |
| [`uml/`](uml/)               | Pipeline state machines, worker lifecycle diagrams                              |
| [`state/`](state/)           | Progress tracking, migration plans                                              |
| [`audit/`](audit/)           | Execution auditor reports                                                       |
| `tools/quality/`             | Quality checking (rails, tables, verification)                                  |
| `tools/refinement/`          | Level assembly (prompts, levels 1-4)                                            |
| `tools/maintenance/`         | Content fixes and gap filling                                                   |
| `tools/benchmark/`           | Benchmark execution                                                             |
| `tools/runners/`             | Pipeline phase runners                                                          |
| `tools/lib/`                 | Core infrastructure + shared helpers                                            |
| `tools/shared/`              | Shared utilities                                                                |
| [`feedback/`](feedback/)     | Inter-agent communication                                                       |

## Pipeline Stages (5-stage)

```
Extraction → Refinement → Merge → Adaptation → Artifacts
(.extracted/)  (.refined/) (.merged/) (.adapted/) (.artifacts/)
```

Run order for the consolidation pipeline: A → B → (B1 if needed) → C → D → E →
F.

## Agents

| #   | Agent                    | Role                                                                                                                                  |
| --- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Extractor                | Reads spec pages, extracts raw text                                                                                                   |
| 2   | Refiner                  | Reformats extracted text into clean markdown                                                                                          |
| 3   | Auditor                  | Verifies claims against disk evidence                                                                                                 |
| 4   | Continuator              | Resumes partial/incomplete work                                                                                                       |
| 5   | SCE Populator            | Generates STE-Code structured data (vocabulary, templates, schemas)                                                                   |
| 6   | STE-Code Analysis        | Paradigm-agnostic (OOP/FP/procedural/systems). Produces STE-Code compliant docs + self-audit                                          |
| 7   | Level Worker             | Parameterized worker. Receives level (1-5) + action (test/rewrite/benchmark), loads rules at that depth                               |
| 8   | Extension Worker         | Generates code-domain gap fillers using batched poll workers. Dictionary entries, category examples, anti-patterns, domain extensions |
| 9   | Translation Orchestrator | Discovery-based locale scaffolding. Blank placeholders for all translatable content across 10 locales                                 |

## Adaptation Levels

| Level  | Content                              | Size   | Tokens | Use Case                                    |
| ------ | ------------------------------------ | ------ | ------ | ------------------------------------------- |
| **-2** | 14 core principles only              | 5 KB   | ~1.2K  | Ultra-minimal, tightest budgets             |
| **-1** | + synonym table                      | 26 KB  | ~5.9K  | Minimal                                     |
| **0**  | + short dictionary excerpt           | 17 KB  | ~4.3K  | Baseline                                    |
| **1**  | + doc templates                      | 58 KB  | ~14.5K | Interactive sessions, low-context scenarios |
| **2**  | + section-specific grammar rules     | 75 KB  | ~18.5K | Code review, PR feedback                    |
| **3**  | + complete dictionary + all 54 rules | 388 KB | ~95K   | Full document rewriting                     |
| **4**  | + extensions + reference catalogue   | 462 KB | ~116K  | Strict compliance checking                  |
| **5**  | Full standard + provenance           | 539 KB | ~134K  | Specification-grade documentation           |

Measured with `python3 .agents/tools/maintenance/measure_artifacts.py`
(o200k_base tokenizer). Rule of thumb for sizing a load: 0.24 tokens per byte of
UTF-8 markdown, i.e. about 4.1 bytes per token.

## Assembly Scripts (all agent-agnostic)

| Script               | Input         | Output           | Description                      |
| -------------------- | ------------- | ---------------- | -------------------------------- |
| `assemble-level1.py` | Level 2       | Level 1 (~14.5K) | Compress to essential principles |
| `assemble-level2.py` | Level 3       | Level 2 (~18.5K) | Compact compliance prompt        |
| `assemble-level3.py` | 54× Level 5   | Level 3 (~95K)   | Section grammar + vocabulary     |
| `assemble-level4.py` | 54× Level 5   | Level 4 (~116K)  | All rules + dictionary excerpt   |
| `sweep-quality.py`   | All artifacts | Sweep report     | 5-batch parallel quality audit   |
| `fix-fixmes.py`      | Adapted files | Fixed files      | Generate missing STE corrections |

All accept `--agent <name>` to use a different backend and `--dry-run` to
preview.

## Benchmark Results (59 tests, 14 categories)

|               | STE-Code      | Plain Assistant | Improvement |
| ------------- | ------------- | --------------- | ----------- |
| **Pass rate** | 96.6% (57/59) | 11.9% (7/59)    | **+84.7%**  |
| **Avg score** | 0.919         | 0.471           | **+0.448**  |

Top 3 categories where STE-Code wins hardest: **comments** (+0.580), **error
messages** (+0.560), **config files** (+0.520).

## Key Artifacts

- `ste-code/artifacts/level1/system-prompt.txt` - Level 1: 14 principles +
  templates (58 KB, ~14.5K tokens)
- `ste-code/artifacts/level2/system-prompt.txt` - Level 2: + section grammar (75
  KB, ~18.5K tokens)
- `ste-code/artifacts/level3/system-prompt.txt` - Level 3: 9-section grammar +
  full dictionary (388 KB, ~95K tokens)
- `ste-code/artifacts/level4/system-prompt.txt` - Level 4: 54 rules +
  dictionary + catalogue (462 KB, ~116K tokens)
- `ste-code/artifacts/level5/system-prompt.txt` - Level 5: full standard +
  provenance (539 KB, ~134K tokens)
- `ste-code/artifacts/llms-full.txt` - every distilled sub-document in one file
- `ste-code/adapted/` - 60 files of ASD-STE100 rules adapted for code (54
  rules + 4 GR + dictionary + categories)
- `.agents/benchmark/orchestrator.py` - Parallel benchmark runner (59 workers,
  CWD-isolated)
- `.agents/benchmark/orchestrator-control.py` - Control group runner (plain
  assistant, no STE-Code)

## Running

```bash
# Assemble level prompts (default: hermes)
python3 .agents/tools/refinement/assemble-level3.py
python3 .agents/tools/refinement/assemble-level2.py
python3 .agents/tools/refinement/assemble-level1.py

# Use a different agent
python3 .agents/tools/refinement/assemble-level1.py --agent claude

# Quality sweep (5 parallel batches)
python3 .agents/tools/quality/sweep-quality.py --batches 5

# STE-Code benchmark (59 tests, parallel)
python3 .agents/benchmark/orchestrator.py

# Control group (plain assistant, same tests)
python3 .agents/benchmark/orchestrator-control.py

# List available agent backends
python3 .agents/tools/lib/agent-runner.py --list
```

## Contributing

See [`.agents/GAPS.md`](GAPS.md) for the full domain coverage gap analysis.

### Quick Start

1. Pick a domain tag from GAPS.md (e.g., `[MOBILE]`, `[ML]`, `[SEC]`)
2. Find the target rule file in `ste-code/adapted/a-secN-ruleX.Y.md`
3. Add Non-STE/STE example pairs using canonical format:

    ```
    > [DOMAIN: mobile]  <!-- tracking placeholder -->
    > **Non-STE:** [realistic code documentation from the domain]
    > **STE:** [STE-Code compliant correction]
    ```

4. Submit a PR with the domain tag in the commit message.

### Domain Placeholders

Active placeholder tags in adapted files mark where domain content belongs:

- `[CONTRIBUTE]` - General contribution welcome
- `[MOBILE]`, `[ML]`, `[GAMEDEV]`, `[EMBEDDED]`, `[WEB3]` - Zero coverage
  domains
- `[SEC]`, `[A11Y]`, `[I18N]`, `[PERF]`, `[TEST]`, `[DOCS]` - High-priority gaps

### Batch Generation (Internal)

```bash
# Generate domain examples across rules
python3 .agents/tools/maintenance/fill-gaps.py --domain MOBILE --rule a-sec4-rule4.3
python3 .agents/tools/maintenance/fill-gaps.py --domain ML --all-rules --min-pairs 3
```

## Skills Inventory

Skills live in buckets under `skills/<bucket>/<skill>/SKILL.md`, distributed to
profiles via two-level symlinks (`link-skills.sh`). A profile loads only its
declared buckets, so the consumer `ste-code` profile is amnesic about
authoring/dev infrastructure.

| Skill             | Bucket / File                                                  | Description                                                                            |
| ----------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Apply Standard    | `skills/ste-code-consumer/apply-standard/SKILL.md`            | The only consumer-facing skill: read the standard, apply it to your own code/docs.      |
| Extraction        | `skills/ste-code-dev/extraction/SKILL.md`                     | 109 parallel workers, 4 pages each, 37 batches                                         |
| Refinement        | `skills/ste-code-authoring/refinement/SKILL.md`               | 9 formatting rules, section-aware v2 workers                                           |
| Grouping (Merge)  | `skills/ste-code-dev/grouping/SKILL.md`                       | Deterministic grouping (concat+split, MANIFEST-driven, no LLM) → `ste-code/grouped/`   |
| Adaptation        | `skills/ste-code-authoring/adaptation/SKILL.md`               | 53 source rules → 54 code-domain rules, 22 categories; orchestrated per-section, gated |
| Artifacts         | `skills/ste-code-authoring/artifacts/SKILL.md`               | Final deliverables assembled from `adapted/`; coverage-verified                        |
| Auditing          | `skills/ste-code-authoring/auditing/SKILL.md`                 | 8-rail verification, fabrication detection                                             |
| Validation        | `skills/ste-code-benchmark/validation/SKILL.md`               | Per-batch quality checks, spot-checks                                                  |
| Continuation      | `skills/ste-code-authoring/continuation/SKILL.md`             | Multi-agent stages 3-5, any agent perspective                                          |
| Benchmarking      | `skills/ste-code-benchmark/benchmarking/SKILL.md`             | 59 tests, 14 categories, control group                                                 |
| Level Worker      | `skills/ste-code-dev/level-worker/SKILL.md`                   | 4 parallel workers at levels 1-4 using agent runner                                    |
| Extension Worker  | `skills/ste-code-authoring/extension-worker/SKILL.md`         | Markdown-first gap-fill generation (orchestrated via `phase-e-run.py`); JSON derived   |
| Translations      | `skills/ste-code-authoring/translations/SKILL.md`             | Multi-locale placeholder pipeline, 10 locales, ~540 files, batch-of-3 workers          |
| State Report      | `skills/ste-code-dev/state-report/SKILL.md`                   | Standardized pipeline state format                                                     |
| Execution Auditor | `skills/ste-code-dev/execution-auditor/SKILL.md`             | Hidden agent for forensic disk verification                                            |
| STE-Code Jail Ops | `skills/ste-code-dev/ste-code-jail-ops/SKILL.md`              | Maintain the jail that confines the three STE-Code Hermes profiles.                    |
| Skill Confinement | `skills/ste-code-dev/hermes-profile-skill-confinement/SKILL.md` | Confine a Hermes profile to a chosen skill set; block default bundled skills.         |

Profile → bucket map (single source, symlinked):

- `dev-ste-code` → `ste-code-dev`, `ste-code-authoring`, `ste-code-benchmark`
- `ste-code` (consumer) → `ste-code-consumer`
- `benchmark-ste-code` → `ste-code-benchmark`

---

## Feedback & Lessons Learned

- [`feedback/exchange.md`](feedback/exchange.md) - Project-specific adaptations
  (2-chain parallelism, gitignore fix, extract_batch.py notes)
- [`feedback/poll-vs-wait.md`](feedback/poll-vs-wait.md) - Use
  `process(action='poll')`, never `wait` or blocking timeouts
- [`feedback/aphrodite-tool-testing.md`](feedback/aphrodite-tool-testing.md) -
  **Use this when working with aphrodite CCR markers**:
  `aphrodite_retrieve(hash=...)` must be called immediately on every
  `<<<CCR:hash|type|size>>>` marker in tool output. Never re-read a file when
  you have a live CCR marker - the marker IS the content.

## See also

- `README.md` - structure + stage table.
- `tools/lib/README.md` - shared helper reference.
- `config/defaults.yaml` - shared agent + runtime defaults.
