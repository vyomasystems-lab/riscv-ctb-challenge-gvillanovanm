# RISCV-DV

Test generation using riscv-dv
```
run --target rv32i --test riscv_arithmetic_basic_test --testlist testlist.yaml --simulator pyflow
```

Coverage related information is obtained in the below link:
https://github.com/chipsalliance/riscv-dv/tree/master/pygen/pygen_src

# Challenge
The challenge is to fix the tool problem in generating coverage and make rv32i ISA coverage 100%

# Report of Activity

The RISCV-DV is _____________________. 
The parameter -i (interaction) control the number of tests.
For example, in the command below, 50 test is made.

```
run --target rv32i --test riscv_arithmetic_basic_test --testlist testlist.yaml --simulator pyflow -v -i 50"
```

To check coverage it's necessary to call the tool cov as follow:

```
cov --dir out_*/spike_sim --enable_visualization  --simulator pyflow
```



```
rm -rf out_2023*
rm -rf cov_out_*

run --target rv32i --test riscv_arithmetic_basic_test --testlist testlist.yaml --simulator pyflow -v -i 50

# cov --dir out_*/spike_sim --enable_visualization  --simulator pyflow
# cat cov_*/CoverageReport.txt
```
Also the testlist.yaml was updated.