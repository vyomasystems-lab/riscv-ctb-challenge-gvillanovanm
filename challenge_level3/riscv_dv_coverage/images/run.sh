rm -rf out_2023*
rm -rf cov_out_*

echo "run --target rv32i --test riscv_arithmetic_basic_test --testlist testlist.yaml --simulator pyflow -v -i NUM_OF_ITERACTIONS"
run --target rv32i --test riscv_arithmetic_basic_test --testlist testlist.yaml --simulator pyflow -v -i 50

cov --dir out_*/spike_sim --enable_visualization  --simulator pyflow
cat cov_*/CoverageReport.txt
