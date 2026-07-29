# Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.12

## Original Rule

**Rule 1.12** You can use verbs that you can include in a technical verb category.

A technical verb is a verb term that refers to a specified concept or process and is applicable to a subject field.

The dictionary does not include technical verbs because there are too many, and each subject field uses different technical verbs for their texts.

You can find many of these technical verbs in your company glossary or terminology database.

STE gives you a list of categories, with examples, to help you:
- Select technical verbs to put in your company glossary or terminology database.
- Use technical verbs correctly.

Technical verbs must obey the same rules as other approved verbs in STE. Refer to section 3.

You can use technical verbs in procedural and descriptive texts if you can include them in one or more of these four categories.

[Original spec lists 4 main categories with subcategories — see master.md lines 2833-2874]

The technical verbs in their related categories are only examples. Rule 1.12 does not give a full list of all possible technical verbs.

If there is an approved verb in the dictionary that accurately gives the instruction or the information, use the approved verb. Do not use a technical verb if it is possible to write the same sentence with the words (verbs and other related words) that are approved in the dictionary.

Examples:

> **Non-STE:** If you detect broken wires, repair them.

("Detect" is not approved and cannot be a technical verb in this context.)

> **STE:** If you find broken wires, repair them.

But you can write:

("Detect" is the correct technical verb in this context.)

If you must use technical verbs, use only technical verbs that are correct in your context. Do not use technical verbs that are general or not clear.

Do not use a technical verb if it is not necessary. If it is possible, use a verb that is approved in the dictionary and an applicable technical noun.

"Clamp" is a technical noun, category 1, official parts information. Do not use "clamp" as a technical verb.
"Grease" is a technical noun, category 4, materials, consumables, and unwanted material. Do not use "grease" as a technical verb.
"Wire" is a technical noun, category 1, official parts information. Do not use "wire" as a technical verb.

The dictionary includes some words that, although not approved, can be technical verbs if you can put them in the specified categories.

> **STE:** Enter your password.

("Enter" is a technical verb, category 2 a), computer processes and applications, input and output processes.)

## STE-Code Adaptation

**Rule 1.12** You can use verbs that you can include in a code-domain technical verb category.

A code-domain technical verb is a verb term that refers to a specified operation or process in software development and is applicable to a subject field.

The controlled terminology does not include all code-domain technical verbs because there are too many, and each project or subject field uses different technical verbs.

You can find many of these code-domain technical verbs in your project glossary or terminology database.

STE-Code gives you a list of categories, with examples, to help you:
- Select code-domain technical verbs to put in your project glossary or terminology database.
- Use code-domain technical verbs correctly.

Code-domain technical verbs must obey the same rules as other approved verbs in STE-Code. Refer to section 3.

You can use code-domain technical verbs in procedural and descriptive texts if you can include them in one or more of these four categories.

1. **Development processes**
   Terms that give instructions and information to:
   a) Write and modify code:
      compile, concatenate, import, inject, instantiate, lint, minify, optimize, polyfill, refactor, resolve, shim, stub, substitute, transpile
   b) Test and verify code:
      assert, benchmark, debug, instrument, mock, profile, spy, stub, unit-test
   c) Build and package:
      bundle, deploy, package, publish, release, tag, version
   d) Manage dependencies:
      hoist, install, link, lock, pin, update, upgrade

2. **Computer processes and applications**
   Terms that give instructions and information for:
   a) Input and output processes:
      click, copy, cut, digitize, enter, paste, press, print, scan, swipe, tap, type
   b) User interface and application operations:
      clear, close, delete, deselect, disable, drag, drag and drop, enable, encrypt, erase, filter, hide, highlight, invalidate, maximize, minimize, navigate, open, save, scroll, select, show, sort, store, submit, toggle, validate, zoom in, zoom out
   c) System operations:
      abort, authenticate, authorize, boot, cache, communicate, configure, debug, download, format, initialize, install, load, log, manage, mount, process, reboot, render, retry, serialize, synchronize, update, upgrade, upload

3. **Instructions and information for applicable subject fields**
   Terms that give instructions and information in these contexts:
   a) Algorithmic, mathematical, and data:
      aggregate, bisect, compute, concatenate, convert, count, encode, escape, filter, hash, index, map, merge, normalize, parse, pipeline, precompute, recalculate, reduce, transform, validate, verify
   b) Database and storage:
      backup, compact, flush, index, migrate, persist, query, replicate, restore, roll back, seed, shard, vacuum, write-ahead
   c) Network and communication:
      broadcast, connect, disconnect, establish, forward, handshake, intercept, listen, poll, proxy, reject, resolve, route, send, stream, timeout, tunnel, unsubscribe
   d) Security and authentication:
      authenticate, authorize, decrypt, encode, encrypt, hash, revoke, salt, sanitize, sign, validate, verify

4. **Legal and licensing terms**
   Terms that give instructions and information only for legal and regulatory texts. For example, licenses, terms of service, contributor agreements, and compliance documents.
   acknowledge, assign, comply with, conform to, disclose, enforce, explain, grant, inform, license, modify, notify, permit, regulate, sign, supersede, waive

The code-domain technical verbs in their related categories are only examples. Rule 1.12 does not give a full list of all possible code-domain technical verbs.

If there is an approved verb in the controlled terminology that accurately gives the instruction or the information, use the approved verb. Do not use a code-domain technical verb if it is possible to write the same sentence with the words (verbs and other related words) that are approved in the controlled terminology.

If you must use code-domain technical verbs, use only code-domain technical verbs that are correct in your context. Do not use code-domain technical verbs that are general or not clear.

Do not use a code-domain technical verb if it is not necessary. If it is possible, use a verb that is approved in the controlled terminology and an applicable code-domain technical noun.

### Examples

> **Non-STE:** If you detect a null pointer exception, fix it.
> **STE:** If you find a null pointer exception, fix it.

"Detect" is not approved in the controlled terminology and is not a code-domain technical verb in this context. The STE version uses the approved verb "find."

> **STE:** The intrusion detection system detects unauthorized access attempts.

"Detect" is a code-domain technical verb (category 3 c), network and communication). In a security context, "detect" is the correct technical term.

> **Non-STE:** Migrate the database schema to version 3.
> **STE:** Run the migration of the database schema to version 3.

"Migrate" is a code-domain technical verb (category 3 b), database and storage), but an approved verb with a code-domain technical noun is possible here. The STE version uses the approved verb "run" and the code-domain technical noun "migration."

> **STE:** Enter your API key in the configuration file.

"Enter" is a code-domain technical verb (category 2 a), computer processes and applications, input and output processes). This word is not approved in the controlled terminology but is permitted because it fits the code-domain technical verb category.
