# Rule 5.3 — Imperative (Command) Form for Instructions

## Original Rule Summary

Rule 5.3 requires that all instructions be written in the imperative (command) form. An instruction tells the reader to do something, and the verb must be in the imperative mood to make the command direct and unambiguous. Passive constructions, modal verbs, and indirect phrasing create ambiguity about whether the reader must act now, whether someone else has already performed the action, or whether someone else will perform it later. Do not use the verb "must" before the imperative form in standard instructions; reserve "must" only for safety warnings or critical conditions.

## STE-Code Adaptation

Rule 5.3 in STE-Code applies the imperative form to all code documentation that tells the reader to execute a command, edit a file, change a setting, or run a script. Every procedural step must start with an imperative verb such as "run," "set," "open," "save," "install," "configure," "restart," "execute," "copy," "delete," "create," "add," "enter," "select," "click," "type," or "verify." Do not use passive voice, gerunds, or modal verbs (such as "can," "could," "should," "may," or "might") for instructions. Descriptive documentation — API endpoint references, docstrings, architecture overviews, and README feature descriptions — may use declarative sentences because they describe system behavior, not reader action.

## Example Pairs

> **Non-STE:** The dependencies can be installed by running `npm install`, and then the server should be started with `npm run dev`.
>
> **STE:** Install the dependencies with `npm install`. Start the server with `npm run dev`.

> **Non-STE:** You can authenticate by sending a POST request to `/auth/login` with your credentials, and you should include the returned token in the `Authorization` header.
>
> **STE:** Send a POST request to `/auth/login` with your credentials. Include the returned token in the `Authorization` header.

> **Non-STE:** Fixed the race condition in the connection pool.
>
> **STE:** Fix the race condition in the connection pool.

## Principles Applied

**P7** — Use the imperative mood for all procedural writing. Rule 5.3 maps directly to P7. Every instruction that tells the reader to act must start with a verb in the imperative form. The imperative mood eliminates the reader's uncertainty about who performs the action, when it must be performed, and whether the action is a requirement or a suggestion. Passive constructions ("The file can be saved"), modal verbs ("you should run"), and past-tense descriptions ("The script was executed") all fail to communicate a direct command. Only the imperative form ("Save the file," "Run the script," "Execute the command") gives the reader an unambiguous instruction.

**P5** — Write one instruction per procedural step. The imperative form enforces the one-action-per-step rule because each imperative verb naturally describes one action. When a writer attempts to pack multiple instructions into a single sentence using modal verbs ("You can install the package and should configure it"), the imperative rewrite forces the writer to split them into separate steps: "Install the package. Configure it." This separation makes each step individually testable and verifiable.

**P13** — Use clear, direct, unambiguous language. Modal verbs and passive constructions introduce three types of ambiguity: (1) temporal ambiguity — the reader cannot tell whether the action must happen now, has already happened, or will happen later; (2) actor ambiguity — the reader cannot tell who must perform the action; (3) obligation ambiguity — the reader cannot tell whether the action is required or optional. The imperative form resolves all three: the command is present-tense (now), directed at the reader (you), and unconditional (do it).

**P4** — Write short sentences. Imperative sentences are structurally shorter than modal or passive equivalents because the imperative omits the subject and the auxiliary verb. Compare "You can install the dependencies by running the setup script" (10 words) with "Install the dependencies with the setup script" (7 words). The imperative form cuts filler words while preserving the instruction's meaning, making documentation faster to scan and easier to translate.
