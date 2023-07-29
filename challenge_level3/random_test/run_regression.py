import os
import shutil
import subprocess
from collections import Counter
import matplotlib.pyplot as plt

# Function to create an instruction histogram
def create_instruction_histogram(file_path):
    instruction_counter = Counter()
    with open(file_path, 'r') as file:
        for line in file:
            instruction = line.strip().split()[0]
            instruction_counter[instruction] += 1
    return instruction_counter

# Function to plot an instruction histogram
def plot_instruction_histogram(instruction_histogram, title):
    instructions, counts = zip(*instruction_histogram.items())
    plt.figure(figsize=(10, 6))
    plt.bar(instructions, counts)
    plt.xlabel('Instructions')
    plt.ylabel('Count')
    plt.title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

# Function to extract values and execute spike-dasm
def extract_values_and_execute(file_path, output_file_path):
    values_list = []
    with open(file_path, 'r') as file:
        for line in file:
            start_index = line.find("(0x") + 3
            end_index = line.find(")", start_index)
            if start_index >= 3 and end_index >= 0:
                value = line[start_index:end_index]
                values_list.append(value)

    with open(output_file_path, 'w') as output_file:
        for value in values_list:
            command = f'echo "DASM({value})" | spike-dasm'
            try:
                output = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
                output_file.write(output)
            except subprocess.CalledProcessError as e:
                output_file.write(f"Error executing command for value {value}: {e.output}\n\n")

# Run regressions
def run_sim_and_move_files(regression_count):
    # Create a directory for the regressions
    os.makedirs("regressions", exist_ok=True)

    # Loop `regression_count` times
    for i in range(1, regression_count + 1):
        print(f"Running regression {i}")

        # make
        subprocess.run(["make"])
        
        # Create a directory for each regression iteration
        reg_dir = f"regressions/reg{i}"
        os.makedirs(reg_dir, exist_ok=True)


        # Move the generated files to the regression directory
        shutil.move("rtl.dump", os.path.join(reg_dir, "rtl.dump"))
        shutil.move("spike.dump", os.path.join(reg_dir, "spike.dump"))
        shutil.move("diff_result.txt", os.path.join(reg_dir, "diff_result.txt"))
        shutil.move("test.S", os.path.join(reg_dir, "test.S"))

# extract_instr_analysis_and_hist
def extract_instr_analysis_and_hist(num_of_reg):
    enable_histogram_plot = 1
    
    for counter in range(num_of_reg):
        idx = counter + 1
        
        # Get the diff between RTL and Spike
        subprocess.run(f"diff -u regressions/reg{idx}/rtl.dump regressions/reg{idx}/spike.dump | grep -E '^\+' | grep -v '+++' | cut -c 2- >> regressions/reg{idx}/diff_bug.txt", shell=True, check=True)

        # Extract and execute spike-dasm
        file_path = f"regressions/reg{idx}/rtl.dump"
        output_file_path = f"regressions/reg{idx}/output_instr.txt"
        extract_values_and_execute(file_path, output_file_path)

        file_path_bug = f"regressions/reg{idx}/diff_bug.txt"
        output_file_path_bug = f"regressions/reg{idx}/output_instr_bug.txt"
        extract_values_and_execute(file_path_bug, output_file_path_bug)

        # Analysis
        instruction_histogram = create_instruction_histogram(output_file_path)
        instruction_histogram_bug = create_instruction_histogram(output_file_path)

        print("# --------------------------------------------------------------------")
        print(f"# Scoreboard / Regression {idx}\n")
        print(f"# Num of instructions total: {len(instruction_histogram.items())}")
        print(f"# Num of matches           : {len(instruction_histogram_bug.items())}")
        print(f"# Num of mismatches        : {len(instruction_histogram.items())-len(instruction_histogram_bug.items())}")
        print("---------------------------------------------------------------------\n")

        if enable_histogram_plot == 1:
            plot_instruction_histogram(instruction_histogram, f"Instructions Stimulated in Reg. {idx}")
            plot_instruction_histogram(instruction_histogram_bug, f"Bugs in Reg. {idx}")

    if enable_histogram_plot == 1:
        plt.show()

if __name__ == "__main__":
    regression_count = 3
    run_sim_and_move_files(regression_count)
    extract_instr_analysis_and_hist(regression_count)

