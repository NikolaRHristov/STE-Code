# STE-Code Domain Extension Templates

> These are placeholder templates for domain-specific content.
> See `.agents/GAPS.md` for the full gap analysis.
> See `.agents/AGENTS.md` for contribution guide.

---

## Template: Adding Domain Examples to a Rule File

When adding domain-specific examples to `ste-code/adapted/a-secN-ruleX.Y.md`,
find the `### Examples` section (or the end of the last example block) and add:

```
> [DOMAIN: tag]  <!-- tracking tag for gap analysis -->

> **Non-STE:** [realistic code documentation from the domain that violates the rule]
> **STE:** [STE-Code compliant correction]

> *Domain: [short description of the domain context]*
```

---

## Placeholder Tags Reference

| Tag | Domain | Priority | Target Rules |
|-----|--------|:--------:|--------------|
| `[MOBILE]` | iOS/Android/Flutter | Critical | sec4, sec5, sec6, sec7, sec16 |
| `[ML]` | Data Science/MLOps | High | sec4, sec6, sec7, sec9, sec14 |
| `[GAMEDEV]` | Game Engines | Medium | sec2, sec6, sec7, sec18 |
| `[EMBEDDED]` | IoT/Firmware | Medium | sec2, sec6, sec9, sec16 |
| `[WEB3]` | Blockchain/Smart Contracts | Low | sec6, sec19, sec21 |
| `[SEC]` | Security Engineering | High | sec7, sec18, sec21 |
| `[A11Y]` | Accessibility | High | sec12, sec17 |
| `[I18N]` | Internationalization | Medium | sec10, sec13, sec16 |
| `[PERF]` | Performance Engineering | Medium | sec7, sec9, sec18 |
| `[TEST]` | Testing Methodologies | High | sec3, sec14, sec22 |
| `[DOCS]` | Documentation Process | High | sec15, sec20 |

---

## Example: Mobile Domain Extension for Rule 4.3 (Vertical Lists)

```
> [DOMAIN: mobile]

> **Non-STE:** The iOS app has a bunch of settings like push notifications on or off, dark mode that follows the system, the language can be English Spanish or French, and you can set the map to use either Apple Maps or Google Maps.
> **STE:** The iOS app has these settings:
> - Push notifications (on or off)
> - Dark mode (system, light, or dark)
> - Language (English, Spanish, or French)
> - Map provider (Apple Maps or Google Maps).

> *Domain: iOS settings screen documentation. Rule 4.3 requires a vertical list for complex enumerations.*
```

---

## Example: ML Domain Extension for Rule 6.3 (Sentence Length)

```
> [DOMAIN: ml]

> **Non-STE:** The `train_model` function loads the preprocessed training dataset from the feature store, initializes the XGBoost classifier with the hyperparameters specified in the experiment config including max_depth=6 learning_rate=0.1 and n_estimators=100, trains the model using 5-fold cross-validation with early stopping after 10 rounds of no improvement, and saves the resulting model artifact to the MLflow model registry with the experiment ID and run metadata for reproducibility.
> **STE:** The `train_model` function loads the training dataset from the feature store. It initializes an XGBoost classifier with these hyperparameters: `max_depth=6`, `learning_rate=0.1`, and `n_estimators=100`. The function trains the model with 5-fold cross-validation. It stops early after 10 rounds with no improvement. It saves the model artifact to the MLflow model registry.

> *Domain: ML model training documentation. Rule 6.3 limits descriptive sentences to 25 words.*
```

---

## Instructions for Batch Workers

To generate domain extensions programmatically:

```bash
# Generate examples for one rule + one domain
python3 .agents/tools/fill-gaps.py \
  --agent hermes \
  --domain MOBILE \
  --rule a-sec4-rule4.3 \
  --min-pairs 3

# Generate across all rules for one domain (5 parallel workers)
python3 .agents/tools/fill-gaps.py \
  --agent hermes \
  --domain ML \
  --all-rules \
  --min-pairs 2 \
  --workers 5
```

Each worker reads the rule, generates domain-specific Non-STE/STE example pairs,
and inserts them with `[DOMAIN: tag]` markers into the file.
