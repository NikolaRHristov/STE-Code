# Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.11

## Original Rule

**Rule 1.11** Do not use different technical nouns for the same item.

When you select a technical noun, do not use a different technical noun in other parts of your text to refer to the same item.

Example:

> **Non-STE:**
> 1. Make sure that the servo control unit is in the open position.
> 2. Do the operational test of the actuator.
> 3. Disconnect the control unit from the test rig.

> **STE:**
> 1. Make sure that the actuator is in the open position.
> 2. Do the operational test of the actuator.
> 3. Disconnect the actuator from the test rig.

In the non-STE example, "servo control unit," "actuator," and "control unit" refer to the same item. Use the technical noun that is approved in your company, industry, or subject field. If, as in the example, the technical noun is "actuator," then always use this technical noun in your text.

## STE-Code Adaptation

**Rule 1.11** Do not use different code-domain technical nouns for the same item.

When you select a code-domain technical noun, do not use a different code-domain technical noun in other parts of your documentation to refer to the same item. Use the code-domain technical noun that is approved in your project, company, industry, or subject field consistently throughout your text.

Changing the name of the same item in different sections of the documentation causes confusion. The reader must determine whether you refer to the same item or to a different item. Always use the same code-domain technical noun for the same item.

### Examples

> **Non-STE:**
> 1. Initialize the UserService class.
> 2. Call the authenticate method on the AccountManager.
> 3. The UserHandler returns a session token.

> **STE:**
> 1. Initialize the UserService class.
> 2. Call the authenticate method on the UserService.
> 3. The UserService returns a session token.

> *Adapted from spec pair: "servo control unit," "actuator," and "control unit" → "actuator" (consistent technical noun). In the spec, three different names refer to the same component, and the reader cannot tell if they are the same or different items. The same problem occurs in code documentation when a class is referred to by three different names. In the non-STE example, "UserService," "AccountManager," and "UserHandler" refer to the same class. The STE version uses the approved code-domain technical noun "UserService" in all three sentences, just as the spec example uses "actuator" consistently.*

> **Non-STE:**
> 1. Send a request to the /api/login path.
> 2. The authentication route returns a JSON Web Token.
> 3. Include the token from the login endpoint in subsequent requests.

> **STE:**
> 1. Send a request to the /api/login endpoint.
> 2. The /api/login endpoint returns a JSON Web Token.
> 3. Include the token from the /api/login endpoint in subsequent requests.

> *Adapted from spec pair: "servo control unit," "actuator," and "control unit" → "actuator" (consistent technical noun). In the spec, three names refer to one item. In the non-STE example, "/api/login path," "authentication route," and "login endpoint" are three names for the same API endpoint. The STE version uses the single approved code-domain technical noun "/api/login endpoint" consistently, just as the spec example uses "actuator" consistently.*
