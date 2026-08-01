## Dictionary excerpt (approved / unapproved)

# STE-Code Adapted Dictionary A-Z

> **Source:** Adapted from ASD-STE100 Issue 9, Part 2 - Dictionary, Pages 149-434
> **Source file:** ste-code/merged/master.md (lines 5591-10976)
> **Generated:** 2026-07-30
> **Domain adaptation:** aerospace → code documentation (API docs, commit messages, README sections, code comments)
> **Preserved:** word alphabetization, STE/non-STE pair format, approved/unapproved status, parts of speech
> **Replaced:** aerospace examples with code examples
> **Approved words:** ~875 (UPPERCASE) | **Unapproved words:** ~1274 (lowercase + UNNAPROVED)

---

## How to Read This Dictionary

- **UPPERCASE words** are approved in STE-Code.
- **lowercase words** are not approved; use the listed alternatives instead.
- **(v)** = verb, **(n)** = noun, **(adj)** = adjective, **(adv)** = adverb, **(prep)** = preposition, **(conj)** = conjunction, **(pron)** = pronoun, **(art)** = article
- **(TN)** = code-domain Technical Noun, **(TV)** = code-domain Technical Verb
- Each entry shows: original rule text → code-domain rewrite → STE/non-STE code example pairs

---

# A

## A (art)
- **Original:** Function word: indefinite article. A FUEL PUMP IS INSTALLED IN ZONE 10.
- **Code-domain:** Function word: indefinite article. A CONFIG FILE IS INCLUDED IN THE ROOT DIRECTORY.
> **STE:** A config file is included in the root directory.
> **Non-STE:** Config files included in root directory.

*Ref: master.md - Dictionary entry A (art), Page 149*

---

## ABANDON (v) - UNNAPROVED
- **Original:** GO (v), STOP (v). IF THERE IS A FIRE, IMMEDIATELY GO TO A SAFE AREA. / IF THE VALUES ARE INCORRECT, STOP THE TEST PROCEDURE.
- **Code-domain:** TERMINATE (v), STOP (v). IF THE BUILD FAILS, STOP THE DEPLOYMENT PIPELINE. / IF THE VALUES ARE INCORRECT, TERMINATE THE TEST RUN.
> **STE:** If the build fails, stop the deployment pipeline.
> **Non-STE:** If the build fails, abandon the deployment pipeline.

> **STE:** If the values are incorrect, terminate the test run.
> **Non-STE:** If the values are incorrect, abandon the test procedure.

*Ref: master.md - Dictionary entry abandon (v), Page 149*

---

## ABILITY (n) - UNNAPROVED
- **Original:** CAN (v). ONE GENERATOR CAN SUPPLY POWER FOR ALL THE SYSTEMS.
- **Code-domain:** CAN (v). ONE CONFIGURATION CAN HANDLE REQUESTS FOR ALL THE ENDPOINTS.
> **STE:** One configuration can handle requests for all the endpoints.
> **Non-STE:** One configuration has the ability to handle requests for all the endpoints.

*Ref: master.md
