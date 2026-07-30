# Rule 8.3 — Use of Parentheses

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.3

## Original Rule

**Rule 8.3** You can use parentheses:

- To make references to illustrations or text
- To include letters or numbers that identify items on an illustration or in a text
- To identify the work steps in a procedure
- To include abbreviations
- To give the singular and plural forms of a noun at the same time
- To explain words or a part of a sentence
- To include an alternative.

In STE, you can use parentheses as follows:

1. To make references to illustrations or text

   > **STE:** Remove the valve (10, Figure 1).
   > **STE:** Install the cover (refer to paragraphs 2 thru 5).

2. To include letters or numbers that identify items on an illustration or in a text

   > **STE:** Disconnect the hoses (2) and (12) from the suction ejector (8).
   > **STE:** Remove the nuts (74), the washers (76), the bolts (68), the seals (70), and the bonding straps (72).

3. To identify the work steps in a procedure

   > **STE:** (1) Install the locking cap (4) on the body (8).
   > **STE:** (2) Safety the locking cap (4) with the cotter pin (5).
   > **STE:** (3) Install a new retaining ring (6).

4. To include abbreviations

   > **STE:** A Liquid Crystal Display (LCD) is a flat-panel display that uses the light-modulating properties of liquid crystals.

5. To give the singular and plural forms of a noun at the same time

   | Example | Text |

   |---------|------|

   | A | Before you do the test(s), install the component(s). |

   | B | Do the applicable test(s). |

6. To explain words or a part of a sentence

   > **STE:** Increase the pressure slowly (not more than 10 psi each minute).
   > **STE:** Make sure that the BLEED pushbutton switch is released (the ON legend is off).

7. To include an alternative

   > **STE:** Open the left (right) access panel L42 (R42).

## STE-Code Adaptation

**Rule 8.3** In code documentation, you can use parentheses:

- To make references to code modules, diagrams, or text
- To include letters or numbers that identify items in a diagram or in a text
- To identify the work steps in a procedure
- To include abbreviations
- To give the singular and plural forms of a noun at the same time
- To explain words or a part of a sentence
- To include an alternative.

1. To make references to code modules, diagrams, or text

   > **STE:** Call the handler (Figure 3, Module A).
   > **STE:** Deploy the service (refer to sections 2 thru 5).

2. To include letters or numbers that identify items in a diagram or in a text

   > **STE:** Disconnect the endpoints (2) and (12) from the load balancer (8).
   > **STE:** Remove the configuration keys (74), the environment variables (76), the secrets (68), the tokens (70), and the certificates (72).

3. To identify the work steps in a procedure

   > **STE:** (1) Install the dependency package (4) in the project directory (8).
   > **STE:** (2) Pin the dependency package (4) with the lock file (5).
   > **STE:** (3) Add a new test case (6).

4. To include abbreviations

   > **STE:** A Command Line Interface (CLI) is a text-based interface that uses typed commands to interact with the operating system.

5. To give the singular and plural forms of a noun at the same time

   > **STE:** Before you run the test(s), set the environment variable(s).

6. To explain words or a part of a sentence

   > **STE:** Increase the timeout slowly (not more than 1000 ms each step).
   > **STE:** Make sure that the DEBUG flag is released (the ON indicator is off).

7. To include an alternative

   > **STE:** Use the left (right) API key for the staging (production) environment.

### Examples

> **Non-STE:** A Representational State Transfer Application Programming Interface, or REST API, is an architectural style for designing networked applications relying on stateless, client-server communication.
> **STE:** A Representational State Transfer Application Programming Interface (REST API) is an architectural style for designing networked applications that uses stateless, client-server communication.
>
> *Adapted from spec pattern: abbreviation in parentheses — "A Liquid Crystal Display (LCD) is a flat-panel display..."*

> **Non-STE:** Run the migration on all database shard servers, the primary and all replica instances, before you deploy.
> **STE:** Run the migration on all database shard(s) before you deploy.
>
> *Adapted from spec pattern: singular/plural in parentheses — "Before you do the test(s), install the component(s)."*
