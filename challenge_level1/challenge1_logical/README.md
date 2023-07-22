# Challenge Level 1 - Logical

In this case, we have encountered two bugs, which will be referred to as 1) Undefined Register and 2) Incorrect Operand. Both issues are presented below:

### Bug 1: Undefined Register

#### Cause

The instruction on line 15852 in "test.S" contains an invalid register. In summary, the RISC-V architecture does not recognize "z4" as a valid register name.

```
and s7, ra, z4 # line 15852 in test.S
```

#### Solution

To resolve this bug, a valid register must be used. RISC-V provides a standard set of register names, such as x0, x1, ..., x31, which are 32 general-purpose registers. These registers are named: zero, ra, sp, gp, tp, t0, t1, ..., s0, s1, ..., a0, a1, etc. Since this context is only for testing, any of these valid registers can be used. In this case, "z4" should be replaced with a valid register "s4," chosen randomly without any specific reason.

```
and s7, ra, s4 # line 15852 in test.S (FIXED)
```

### Bug 2: Incorrect Operand

#### Cause

The instruction on line 25581 in "test.S" contains an invalid operand. Specifically, the last operand in ADDI should be a 12-bit value.

```
and s5, t1, s0 # line 25581 in "test.S
```

#### Solution

Two solutions are possible to fix this bug: 

1) Change "s0" to a 12-bit constant.
2) Change the "addi" instruction to "add".

To maintain the pattern of "test.S," it was chosen to update the instruction to "add".

```
add s5, t1, s0 # line 25581 in "test.S" (FIXED)
```

By implementing these fixes, both bugs are resolved, and the assembly code should function correctly as intended.
