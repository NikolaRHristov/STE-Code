# Rule 3.7 — Use an approved verb to describe an action, not a noun or other parts of speech.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.7

> Source: master.md#sec3-rule3.7

## Original Rule

There can be different solutions to give the same information in STE. If there is an approved verb that describes an action, use the approved verb. Verbs describe actions more clearly than nouns or other parts of speech.

> **Non-STE:** Do not write: The ohmmeter gives an indication of 450 ohms.
>
> **STE:** WRITE: The ohmmeter shows 450 ohms.
>
> **Non-STE:** Do not write: Before the removal of the unit, make sure that the power supply is OFF.
>
> **STE:** WRITE: Before you remove the unit, make sure that the power supply is OFF.

In the examples, all sentences are in STE but those with direct verbs describe the action more clearly.

If a word is not approved as a verb in the dictionary, do not use it as a verb. Use a different sentence construction to give the same information.

> **Non-STE:** Check the laptop battery.
>
> **STE:** Do a check of the laptop battery.

## STE-Code Adaptation

There can be different solutions to give the same information in STE-Code. If there is an approved verb that describes an action, use the approved verb. Verbs describe actions more clearly than nouns or other parts of speech.

The four approved Technical Code Verb categories give you the verbs that you can use to describe an action:

1. **Development operations** — build, compile, test, lint, format, commit, push, deploy, rollback
2. **Data operations** — read, write, serialize, deserialize, parse, encode, decode, query, insert, migrate
3. **Application operations** — handle, route, authenticate, authorize, validate, schedule, dispatch, resolve
4. **Communication operations** — send, receive, publish, subscribe, stream, poll, broadcast, connect

If a word is not approved as a verb in the STE-Code dictionary, do not use it as a verb. Use a different sentence construction (usually the noun form of the word) to give the same information.

## Examples

> **Non-STE:** The profiler gives an indication of 200ms latency.
>
> **STE:** The profiler shows 200ms latency.
>
> *Adapted from spec pair: "The ohmmeter gives an indication of 450 ohms." / "The ohmmeter shows 450 ohms." The approved verb "show" describes the action more clearly than the noun phrase "gives an indication of."*

> **Non-STE:** Before the initialization of the service, make sure that the config is valid.
>
> **STE:** Before you initialize the service, make sure that the config is valid.
>
> *Adapted from spec pair: "Before the removal of the unit, make sure that the power supply is OFF." / "Before you remove the unit, make sure that the power supply is OFF." Use the approved verb "initialize" instead of the noun "initialization."*

> **Non-STE:** Cache the response.
>
> **STE:** Do a cache of the response.
>
> *Adapted from spec pair: "Check the laptop battery." / "Do a check of the laptop battery." "Cache" is an approved technical noun (category 7) but not an approved verb. Use the noun form "Do a cache" instead of the verb "Cache."*

> **Non-STE:** Do not write: The function gives a result of 500 OK.
>
> **STE:** The function returns 500 OK.
>
> *Adapted from spec principle: the approved verb "return" describes the action more clearly than the noun phrase "gives a result of."*
