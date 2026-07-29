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

In the non-STE example, "UserService," "AccountManager," and "UserHandler" refer to the same class. The reader cannot determine if these are different classes or the same class with different names. Use the code-domain technical noun that is approved in your project. If the approved class name is "UserService," then always use "UserService" in your documentation.

> **Non-STE:**
> 1. Send a request to the /api/login endpoint.
> 2. The authentication route returns a JSON Web Token.
> 3. Include the token from the login path in subsequent requests.

> **STE:**
> 1. Send a request to the /api/login endpoint.
> 2. The /api/login endpoint returns a JSON Web Token.
> 3. Include the token from the /api/login endpoint in subsequent requests.

In the non-STE example, "/api/login endpoint," "authentication route," and "login path" refer to the same API endpoint. The STE version uses the same code-domain technical noun "/api/login endpoint" in all three sentences.
