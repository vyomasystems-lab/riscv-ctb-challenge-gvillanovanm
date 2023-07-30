import os
import shutil
import subprocess
from collections import Counter
import matplotlib.pyplot as plt

def print_fail():
    str = r"""
 /$$$$$$$$/$$$$$   /$$$$$$ /$$      
| $$_____/$$__  $$|_  $$_/| $$      
| $$    | $$  \ $$  | $$  | $$      
| $$$$$ | $$$$$$$$  | $$  | $$      
| $$__/ | $$__  $$  | $$  | $$      
| $$    | $$  | $$  | $$  | $$      
| $$    | $$  | $$ /$$$$$$| $$$$$$$$
|__/    |__/  |__/|______/|________/
                                    
                                    
                                    """
    print(str)

def print_pass():
    str = r"""
 /$$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$ 
| $$__  $$ /$$__  $$ /$$__  $$/$$__  $$
| $$  \ $$| $$  \ $$| $$  \__/ $$  \__/
| $$$$$$$/| $$$$$$$$|  $$$$$$|  $$$$$$ 
| $$____/ | $$__  $$ \____  $$\____  $$
| $$      | $$  | $$ /$$  \ $$/$$  \ $$
| $$      | $$  | $$|  $$$$$$/  $$$$$$/
|__/      |__/  |__/ \______/ \______/ 
                                    
                                    
                                    """
    print(str)

def print_bugs():
    folder_path = './regression'
    output_file_path = 'concatenated_bugs.txt'
    with open(output_file_path, 'w') as output_file:
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename == 'instr_buggy.txt':
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r') as input_file:
                        output_file.write(input_file.read())

    # Read and print the content of the concatenated_bugs.txt file
    with open(output_file_path, 'r') as concatenated_file:
        print(concatenated_file.read())

# Function to create an instruction histogram
def instruction_counter(file_path):
    instruction_counter = Counter()
    with open(file_path, 'r') as file:
        for line in file:
            instruction = line.strip().split()[0]
            instruction_counter[instruction] += 1
    return instruction_counter

# Function to extract values and execute spike-dasm
def transform_hex_in_mnemonics(file_path, output_file_path):
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

# Run regression
def run(regression_count):
    num_of_tests = 0
    num_of_match = 0
    num_of_mismatch = 0

    # Create a directory for the regression
    os.makedirs("regression", exist_ok=True)

    # Loop `regression_count` times
    for idx in range(1, regression_count + 1):
        print(f"# -------------------------------------------------------------------")
        print(f"#")
        print(f"# Running test {idx}")
        print(f"#")
        print(f"# -------------------------------------------------------------------")

        # -----------------------------------------------------
        # STEP 1: create/run a test
        # -----------------------------------------------------

        # Create/run the test (artefacts)
        subprocess.run(["make"])
                
        # --------------
        # Save artefacts
        # --------------
        
        # Create a directory for each test and move it
        reg_dir = f"regression/test{idx}"
        os.makedirs(reg_dir, exist_ok=True)

        # Move artefacts
        shutil.move("rtl.dump", os.path.join(reg_dir, "rtl.dump"))
        shutil.move("spike.dump", os.path.join(reg_dir, "spike.dump"))
        shutil.move("diff_result.txt", os.path.join(reg_dir, "diff_result.txt"))
        shutil.move("test.S", os.path.join(reg_dir, "test.S"))

        # -----------------------------------------------------
        # STEP 2: compare
        # -----------------------------------------------------

        # Compute the diff between DUT and refmod ("compare") -> test<num>/diff_bug.txt
        subprocess.run(f"diff -u regression/test{idx}/rtl.dump regression/test{idx}/spike.dump | grep -E '^\+' | grep -v '+++' | cut -c 2- >> regression/test{idx}/diff_bug.txt", shell=True, check=True)

        # Transform hex of diff in a literal instruction
        path_diff_bug = f"regression/test{idx}/diff_bug.txt"
        path_mnemonic_diff_bug = f"regression/test{idx}/instr_buggy.txt"
        transform_hex_in_mnemonics(path_diff_bug, path_mnemonic_diff_bug)

        # Transform the rtl or spike hex to analysis before 
        path_instr_dump = f"regression/test{idx}/rtl.dump"
        path_mnemonic_instr_dump = f"regression/test{idx}/instr_dump.txt"
        transform_hex_in_mnemonics(path_instr_dump, path_mnemonic_instr_dump)

        instruction_counter_in_diff_bug = instruction_counter(path_mnemonic_diff_bug)
        
        if len(instruction_counter_in_diff_bug.items()) > 0:
            print_fail()
            print(f"# -------------------------------------------------------------------")
            print(f"# Bug information:\n#")
            print(f"# Test num. {num_of_tests}")
            print(f"# {instruction_counter_in_diff_bug}")
            print(f"# -------------------------------------------------------------------\n\n\n")
            num_of_mismatch = num_of_mismatch + 1
        else:
            print_pass()
            num_of_match = num_of_match + 1

        num_of_tests = num_of_tests + 1
    
    # -----------------------------------------------------
    # STEP 3: end of the test / scoreboard
    # -----------------------------------------------------
    print(f"# -------------------------------------------------------------------")
    print(f"# Scoreboard\n#")
    print(f"# Num of tests      : {num_of_tests}")
    print(f"# Num of matches    : {num_of_match}")
    print(f"# Num of mismatches : {num_of_mismatch}")
    print(f"#")
    print(f"# Bugs instructions :")
    if num_of_mismatch == 0:
        print("(none)")
    else:
        print_bugs()
    print(f"# ------------------------------------------------------------------\n\n")

if __name__ == "__main__":
    num_of_tests = 100
    run(num_of_tests)

