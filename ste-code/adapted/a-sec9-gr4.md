# GR-4 — The Pronoun "This"

> **Source:** Adapted from ASD-STE100 Issue 9, GR-4

## Original Rule

The pronoun "this" (general recommendation, not an STE rule).

When you use the pronoun "this" in a sentence, make sure that the reader knows the item the pronoun refers to. If "this" can refer to more than one item, give the applicable context again.

## STE-Code Adaptation

> **See also:** GR-1 — The Conjunction "That"; GR-2 — The Preposition "With"; GR-3 — How to Use Pronouns

In code documentation, when you use the pronoun "this" in a sentence, make sure that the reader knows exactly which item, condition, or result the pronoun refers to. If "this" can refer to more than one item in the preceding text, repeat the applicable context to remove the ambiguity.

In software documentation, "this" frequently refers to a condition, an error state, a configuration, or a result described in the previous sentence. If the reader cannot immediately identify the referent, the instruction or explanation becomes unclear and can lead to incorrect implementation.

### Examples

> **Non-STE:** Make sure that the connection is not closed. If it is, this can cause failure of the request.
>
> (Does "this" refer to the connection in the closed condition or to the connection in the not-closed condition?)

> **STE:** Make sure that the connection is not closed. If the connection is closed, this can cause failure of the request.

(The context is repeated so that the reader knows "this" refers to the closed condition.)
*Adapted from spec pair: "Make sure that the cover is not locked. If it is, this can cause damage to the probe." / "Make sure that the cover is not locked. If the cover is locked, this can cause damage to the probe."*

Or:

> **STE:** If the connection is closed, failure of the request can occur.

*Adapted from spec alternative: "If the cover is locked, damage to the probe can occur."*

> **Non-STE:** Check that the environment variable is set. If it is not, this can prevent the build from completing.
>
> (Does "this" refer to the variable being not set, or to the act of checking?)

> **STE:** Check that the environment variable is set. If the environment variable is not set, this condition can prevent the build from completing.

*Adapted from spec pattern: repeat the applicable context to disambiguate "this."*

> **Non-STE:** Verify that the function returns a non-null value. If it does not, this can cause a runtime error in the caller.
>
> **STE:** Verify that the function returns a non-null value. If the function returns a null value, this null value can cause a runtime error in the caller.

*Adapted from spec pattern: replace the pronoun with the explicit referent to remove ambiguity.*

> **Non-STE:** The server validates the token and then processes the request. This can take several seconds.
>
> (Does "This" refer to the validation, to the request processing, or to both?)
>
> **STE:** The server validates the token and then processes the request. The full validation and processing sequence can take several seconds.
>
> *Adapted from spec pattern: repeat the applicable context to disambiguate "This."*
>
> (The context is repeated so that the reader knows "This" refers to both actions together.)

> **Non-STE:** Make sure the cache is not stale. This can cause incorrect data to be returned.
>
> (Does "This" refer to the cache being stale or to the act of making sure?)
>
> **STE:** Make sure the cache is not stale. A stale cache can cause incorrect data to be returned.
>
> *Adapted from spec pattern: repeat the applicable context to disambiguate "This."*
>
> (Replacing "This" with "A stale cache" clarifies that the stale condition causes the problem.)

> **Non-STE:** The function accepts a callback and a timeout parameter. This is optional.
>
> (Does "This" refer to the callback, to the timeout parameter, or to both?)
>
> **STE:** The function accepts a callback and a timeout parameter. The timeout parameter is optional.
>
> *Adapted from spec pattern: repeat the applicable context to disambiguate "This."*
>
> (The specific noun "The timeout parameter" replaces "This" to remove the ambiguity.)

> **Non-STE:** Run the migration script and restart the server. This can cause downtime.
>
> (Does "This" refer to running the migration, restarting the server, or both?)
>
> **STE:** Run the migration script and restart the server. Restarting the server can cause downtime.
>
> *Adapted from spec pattern: repeat the applicable context to disambiguate "This."*
>
> (The explicit referent "Restarting the server" tells the reader which action causes the downtime.)

> **Non-STE:** The build pipeline compiles the source and runs the test suite. If this fails, check the logs.
>
> (Does "This" refer to the compilation, the test suite, or the entire pipeline?)
>
> **STE:** The build pipeline compiles the source and runs the test suite. If the test suite fails, check the logs.
>
> *Adapted from spec pattern: repeat the applicable context to disambiguate "This."*
>
> (The specific referent "the test suite" replaces "this" to tell the reader what to check.)

> **Non-STE:** The middleware checks the rate limit and the authentication state. This must be configured in the settings file.
>
> (Does "This" refer to the middleware, the rate limit, the authentication state, or all of them?)
>
> **STE:** The middleware checks the rate limit and the authentication state. The rate limit and the authentication state must be configured in the settings file.
>
> *Adapted from spec pattern: repeat the applicable context to disambiguate "This."*
>
> (The explicit referents "The rate limit and the authentication state" remove the ambiguity.)

> **Non-STE:** The logger writes to stdout and to a file. You can disable this in the configuration.
>
> (Does "This" refer to stdout output, file output, or both?)
>
> **STE:** The logger writes to stdout and to a file. You can disable file logging in the configuration.
>
> *Adapted from spec pattern: repeat the applicable context to disambiguate "This."*
>
> (The specific term "file logging" replaces "this" to tell the reader which output is affected.)

> **Non-STE:** The API returns a status code and a response body. This indicates whether the request succeeded.
>
> (Does "This" refer to the status code, the response body, or both?)
>
> **STE:** The API returns a status code and a response body. The status code indicates whether the request succeeded.
>
> *Adapted from spec pattern: repeat the applicable context to disambiguate "This."*
>
> (Replacing "This" with "The status code" specifies which part of the response carries the success indicator.)
