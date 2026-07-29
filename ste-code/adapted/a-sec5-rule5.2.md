# Rule 5.2 — One Instruction Per Sentence

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.2

## Original Rule

Write only one instruction in each sentence unless two or more actions occur at the same time.

If there are too many instructions in a sentence, the sentence is not easy to read and understand.

Write only one instruction in each sentence and clearly show (usually with numbers or letters) the sequence of the work steps. You can use as many work steps as you want in a procedure.

Examples:

> **STE:** (1) Set the TEST switch to the middle position.
> **STE:** (2) Make sure that all the switches on the control panel are OFF.

(Two work steps)

> **Non-STE:** Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover. (25 words)
> **STE:** Put preservation oil into the unit through the vent hole. (10 words) Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover. (16 words)

Examples of actions that occur at the same time:

- Hold the panel in its open position and install the fastener.
- Slowly extend the rod fully and make sure that it does not touch other parts.
- Cut and remove the wire.
- Remove and discard the seal.

## Procedures

You can write more than one sentence in a work step:

- When actions occur at the same time
- When a result occurs immediately after an action.

Examples in STE:

Make sure that the locking torque of each of the four bolts (6) is a minimum of 0.30 Nm. Then, torque each of the four bolts (6) to 4.20 Nm.

(During a torque procedure, the torque action immediately follows the check of the locking torque in one action. Thus, you cannot divide the sentence into two different work steps.)

Measure the leakage from the outlet port. The leakage must not be more than 0.5 cc/minute.

(The second sentence here gives the limit for the result of the test. The work step occurs in one action, and you cannot divide the sentence into two different work steps.)

## STE-Code Adaptation

In code documentation, procedural steps must be easy for the reader to execute one at a time. When a sentence contains multiple instructions, the reader can miss or skip an action, leading to errors in configuration, deployment, or debugging.

Write only one instruction for the reader to perform in each sentence. Use numbered or bulleted lists to show the sequence of steps clearly. There is no limit on the number of work steps in a procedure.

You may write two instructions in one sentence with the conjunction "and" only when both actions must occur at the same time and cannot be separated into distinct steps. Examples include operations where the reader must hold one state while performing another action, or where two actions are part of a single continuous motion.

You may write more than one sentence in a single work step when:

- Two or more actions occur at the same time and are inseparable
- A result or measurement occurs immediately after an action, and describing them in separate steps would break the logical flow of the procedure.

### Examples

> **Non-STE:** Open the configuration file in a text editor and locate the database section and change the connection string to point to the staging server and then save the file and close the editor. (37 words, 5 instructions)
> **STE:** (1) Open the configuration file in a text editor. (2) Locate the database section. (3) Change the connection string to point to the staging server. (4) Save the file. (5) Close the editor.

(Each instruction is a separate work step.)

> **Non-STE:** Run the test suite with the coverage flag enabled and verify that the total line coverage is above 80 percent across all modules in the project. (27 words)
> **STE:** Run the test suite with the coverage flag enabled. (9 words) The total line coverage must be more than 80 percent across all project modules. (14 words)

(The second sentence states the result limit. The work step is one action and cannot be divided into two separate work steps.)

> **Non-STE:** Make sure the environment variable DATABASE_URL is set correctly and then execute the initialization script to create the required database tables and populate them with the seed data. (31 words)
> **STE:** Make sure that the environment variable DATABASE_URL is set correctly. Then, execute the initialization script. The script creates the required database tables and populates them with the seed data.

(The check and the execution form one continuous work step. The third sentence explains what the script does.)

Actions that occur at the same time:

- Hold the Shift key and click the Reload button.
- Press and release the reset button on the device.
- Copy and replace the existing configuration file.
- Download and extract the archive to the target directory.

> **Non-STE:** Set the logging level to debug mode and then restart the application server and after that monitor the log output in the terminal for any error messages that appear during the startup sequence. (35 words)
> **STE:** (1) Set the logging level to debug. (2) Restart the application server. (3) Monitor the terminal log output for error messages during the startup sequence.

(Three separate instructions, three work steps.)
