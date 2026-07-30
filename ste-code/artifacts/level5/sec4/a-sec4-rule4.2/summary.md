# Rule 4.2 — Do Not Omit Words or Use Contractions to Make Your Sentences Shorter

## Original Rule Summary

Rule 4.2 requires that every sentence in technical writing have all its grammatical parts — subject, verb, nouns, and articles — without omission. The rule prohibits contractions (for example, "don't," "isn't," "aren't") because they combine words by removing letters and inserting an apostrophe, which makes parsing harder for non-native readers. A sentence that is made shorter by omitting words or using contractions is not necessarily easier to read; the shorter form often creates ambiguity about who acts, what the action is, and which object is affected. The rule applies to all five types of omission: omitted subjects, omitted verbs, omitted nouns, omitted articles, and contracted word forms.

## STE-Code Adaptation

Rule 4.2 in STE-Code applies the no-omission requirement across all code documentation types — README files, API documentation, docstrings, inline comments, error messages, and commit message body text. Writers must include the subject in every sentence so the reader always knows which function, class, module, or system component performs the action; they must include the verb so the action is explicit; they must include nouns so every code element referenced is named; and they must include articles ("the," "a," "an") so the reader can distinguish specific instances from general types. Contractions are prohibited in all prose because they are not approved word forms in the controlled terminology, they obscure the auxiliary verb and negation, and the apostrophe character creates visual ambiguity with code syntax (string literals, character literals, atom literals). The adaptation preserves the rule's core test: before publishing, verify that every sentence has a subject, a verb, all necessary nouns and articles, and zero contractions.

## Example Pairs

> **Non-STE:** Can accept a string or a Buffer. Returns the parsed result. Doesn't throw on invalid input.
>
> **STE:** The function can accept a string or a Buffer object. The function returns the parsed result. The function does not throw an error on invalid input.
>
> *(P8 applied: the omitted subject is restored — each sentence now identifies "The function" as the actor. P1 applied: the contraction "Doesn't" is expanded to the approved full form "does not." P4 applied: the expanded auxiliary "does not" uses the approved simple-present verb form.)*

>
> **Non-STE:** Copy `.env.example` to `.env` and update database URL. The app won't run if this step isn't done.
>
> **STE:** Copy the `.env.example` file to a `.env` file. Update the database URL in the `.env` file. The application will not run if this step is not completed.
>
> *(P8 applied: omitted articles are restored — "the `.env.example` file," "a `.env` file," "the database URL," "the `.env` file" now specify which file is which. P1 applied: contractions "won't" and "isn't" are expanded to "will not" and "is not." P3 applied: the complete form is the simpler construction — no reader must guess whether ".env" is a file or a directory.)*

>
> **Non-STE:** The token expired. Server doesn't accept it for new requests.
>
> **STE:** The access token is expired. The server does not accept the token for new requests.
>
> *(P8 applied: the omitted verb "is" is restored in "The access token is expired." The omitted subject "The server" is added so the reader knows which component rejects the token. P1 applied: the contraction "doesn't" is expanded to "does not." P4 applied: the noun "token" is clarified to "access token" to remove ambiguity about which token is referenced.)*

## Principles Applied

**P8** — Use clear, direct, unambiguous language. This is the primary principle for Rule 4.2. An omitted subject leaves the reader guessing which function, class, or module performs the action. An omitted verb leaves the reader guessing what the action is. An omitted noun leaves the reader guessing which code element is affected. An omitted article leaves the reader guessing whether a noun is a specific instance or a general type. Restoring every omitted word removes all four types of ambiguity and makes each sentence self-contained.

**P1** — Use approved words from the controlled terminology. Contractions like "don't," "isn't," "aren't," "won't," and "can't" are not approved word forms in the STE-Code vocabulary. The full forms — "do not," "is not," "are not," "will not," "cannot" — are the approved alternatives. Expanding every contraction ensures that every word in the sentence is an approved word or an approved form.

**P4** — Use only approved verb forms and tenses. Contractions obscure the verb form. The contraction "doesn't" hides the auxiliary verb "does" (third-person singular, simple present) and fuses it with the negation "not." The full form "does not" makes the verb visible and keeps the negation separate. This separation is essential in code documentation where verb tense and subject-verb agreement carry meaning about state (is the action ongoing or completed?).

**P3** — Prefer the simpler construction. A shorter sentence achieved by omission is not necessarily simpler. A sentence that reads "Can accept a string or a Buffer" (4 content words) is shorter than "The function can accept a string or a Buffer object" (10 words), but the shorter version forces the reader to infer the subject from context. The complete version is the simpler construction because the reader does not need to infer anything — all information is present in the sentence.
