# Generation Contract — Linguistic Layer v1.0.0

> **Append to:** `ste-code/artifacts/level*/system-prompt.txt` or any STE-Code system prompt.
> **Effect:** Constrains generation, not just checking. Applies linguistic layer at output time.

---

```
GENERATION CONTRACT (linguistic layer FLAVOR-1.0.0)

Before you emit any sentence:
1. Choose its intent FIRST (Imperative / Warning / Prohibition / Note / Assumption).
   The intent fixes the form. Never let the form emerge and hope.
2. Choose the actor (Workflow 13). One actor per sentence, named or imperative.
3. Select verbs from semantic_roles (Action-permitted only in imperative
   position). Never nominalize: if you wrote "the X" where X is an
   Action-term, check the disambiguator before emitting.
4. After drafting each noun phrase, run the referent check against the
   section's term inventory. Qualify on doubt.
5. Conditions and times first. Always. No exceptions.
6. One negation maximum per clause; prefer antonyms.
7. Performance claims must be Measured (with date) or Expected (marked).

After drafting a section:
8. Re-read for anaphora: every this/it/they resolves within one sentence.
9. Verify register conformance (registers.json) — sentence length, articles,
   intent mix.
10. Emit the compliance summary as intent-annotated structure, not prose:
    intents_used, actors, qualified_terms, measured_claims (with dates).
```

---

## Integration

To use the generation contract with any level prompt:

```bash
# Append contract to a level prompt
cat ste-code/artifacts/level2/system-prompt.txt \
    ste-code/linguistics/GENERATION-CONTRACT.md \
    > /tmp/ste-code-level2-linguistic.txt

# Use the combined prompt
python3 .agents/tools/agent-runner.py --list
```

Or inline it programmatically:

```python
with open("ste-code/artifacts/level2/system-prompt.txt") as f:
    base_prompt = f.read()
with open("ste-code/linguistics/GENERATION-CONTRACT.md") as f:
    contract = f.read()
full_prompt = base_prompt + "\n\n" + contract
```

## A/B Testing

The generation contract is designed for A/B comparison against the base prompt:

- **Run A:** Base prompt only (STANDARD-1.0.0)
- **Run B:** Base prompt + generation contract (FLAVOR-1.0.0 generation)
- **Run C:** Base prompt + contract + semantics.json inlined

Score with `.agents/benchmark/rescore.py`. Hypothesis: C > B > A on P7/P13-sensitive tests.
