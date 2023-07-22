# Challenge: AAPG Generation Test

## Challenge Specification

The challenge is to create an AAPG (Automated Assembly Program Generator) config file that generates a test with 10 illegal exceptions, each with the correct handler code.

## Solution

To complete this challenge, the following steps were followed:

1. The config file used in "challenge_level2/challenge_instructions" was copied to this directory.
2. The line in "rv32i.yaml" was updated from:

   ```
   ecause02: 0
   ```

   to:

   ```
   ecause02: 9
   ```

3. The AAPG tool was run.

The reason for using "9" instead of "10" was due to the output log test, as shown below. Using "9" resulted in 10 exceptions, in accordance with the challenge specification.

```
...
grep trap_illegal_instruction spike.log > exceptions.log
cat exceptions.log
core   0: exception trap_illegal_instruction, epc 0x800000b0
core   0: exception trap_illegal_instruction, epc 0x80000704
core   0: exception trap_illegal_instruction, epc 0x80000cb4
core   0: exception trap_illegal_instruction, epc 0x80000cdc
core   0: exception trap_illegal_instruction, epc 0x80000db8
core   0: exception trap_illegal_instruction, epc 0x800013f4
core   0: exception trap_illegal_instruction, epc 0x8000150c
core   0: exception trap_illegal_instruction, epc 0x80001524
core   0: exception trap_illegal_instruction, epc 0x80001548
core   0: exception trap_illegal_instruction, epc 0x800015f8
wc -l exceptions.log
10 exceptions.log
```

## <!> IMPORTANT NOTE: DO WE HAVE A BUG IN AAPG? <!>

When executing the config file presented in the last section, the output was not always the same. Sometimes, after execution, the simulation never stopped, and other times, the simulation stopped and returned the log presented in the last section.

Attempts were made to create some modifications in "rv32i.yaml," but the same behavior persisted. It is suspected that there may be a bug in AAPG that causes this inconsistent behavior. Further investigation is needed to resolve this issue.
