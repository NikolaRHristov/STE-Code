# Rule 3.1 — Use only the verb forms that are given in the dictionary.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.1

> Source: master.md#sec3-rule3.1

## Original Rule

The STE dictionary gives you the verb forms that you can use for each approved verb. Use only the verb forms that are given in the dictionary.

```
REMOVE (v)
REMOVES
REMOVED,
REMOVED

GIVE (v)
GIVES
GAVE,
GIVEN
```

> **Source:** Issue 9, Part 1 — Writing rules, Page 1-3-1, 2025-01-15

The introduction to the dictionary in part 2 gives you more information about the verb forms and how to use the approved verbs.

> **See also:** Rule 3.1 — Use only the verb forms that are given in the dictionary.

## STE-Code Adaptation

The STE-Code dictionary gives you the verb forms that you can use for each approved verb. Use only the verb forms that the dictionary gives for a verb. Do not use other forms (for example, gerunds, participles used as verbs with auxiliaries, or inflected forms that are not listed).

Every approved verb in the STE-Code dictionary appears with its allowed forms. The dictionary shows the base form, the third-person singular, the simple past, and the past participle. You use only those forms.

```
VALIDATE (v)
VALIDATES
VALIDATED,
VALIDATED

WRITE (v)
WRITES
WROTE,
WRITTEN
```

The four approved verb categories in STE-Code are:

1. **Development operations** — build, compile, test, lint, format, commit, push, deploy, rollback
2. **Data operations** — read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate
3. **Application operations** — handle, route, authenticate, authorize, validate, schedule, dispatch, resolve
4. **Communication operations** — send, receive, publish, subscribe, stream, poll, broadcast, connect

When you write a verb, confirm that the form is one that the dictionary lists for that verb. If the verb is not in the dictionary, do not use it. Use an approved verb instead.

> **Note: structural carryover — no code-domain equivalent** — The dictionary layout (base form, third-person singular, simple past, past participle shown for each verb) is a structural feature of the source standard. The code-domain version keeps the same layout with code verbs. No mapping is forced.

## Examples

> **Non-STE:** The linter validates the file and is reporting the errors to the terminal.
> **STE:** The linter validates the file. It reports the errors to the terminal.
>
> *Adapted from spec principle: use only the verb forms that the dictionary gives. The progressive form "is reporting" is not an approved form.*

> **Non-STE:** The script has written the output to the log before the test starts.
> **STE:** The script wrote the output to the log. Then the test starts.
>
> *Adapted from spec principle: use only the approved simple past form. The present perfect "has written" is not an approved form.*

> *Adapted from spec pair:* Non-STE: <u>The operator has adjusted the linkage.</u> (The present perfect tense is not approved.)  |  STE: The operator adjusted the linkage. (The simple past tense is approved.)
