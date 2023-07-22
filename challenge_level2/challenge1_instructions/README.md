# Bug: Unrecognized Opcode

## Description

The aapg (Automated Assembly Program Generator) supports different kinds of RISC-V extensions. The provided config file "rv32i.yaml" is used to configure the desired extension and other characteristics of the design.

In this case, the bug has occurred due to the addition of RV64M instructions. These instructions are added despite the fact that the design under test is based only on RV32I. As a result, the assembler returns many errors of the type "Error: unrecognized opcode" whenever it encounters a non-supported instruction, i.e., RV64M.

## Solution

To resolve this bug, it is necessary to update (turn off) the generation of RV64M instructions. To do this, change the code below from:

```assembly
rel_rv64m: 10
```

to:

```assembly
rel_rv64m: 0
```

By making this modification, the aapg will no longer generate RV64M instructions, ensuring that the assembler doesn't encounter any "unrecognized opcode" errors.
