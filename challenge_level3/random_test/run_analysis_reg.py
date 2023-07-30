import os
import matplotlib.pyplot as plt
from tabulate import tabulate

# List of RISC-V instructions
INSTRUCTIONS = [
    "add", "sub", "xor", "or", "and", "sll", "srl", "sra", "slt", "sltu",
    "addi", "xori", "ori", "andi", "slli", "srli", "srai", "slti", "sltiu",
    "lb", "lh", "lw", "lbu", "lhu", "sb", "sh", "sw",
    "beq", "bne", "blt", "bge", "bltu", "bltz", "bgeu",
    "j", "jal", "jalr", "lui", "auipc",
    # "ecall",
    # RISC-V CSR Instructions
    "csrr", "csrs", "csrrw", "csrrs", "csrrc", "csrrwi", "csrrsi", "csrrci",
]

def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [line.split()[0] for line in data]  # Extract the first string of each line

def concatenate_data_from_files(root_folder, target_file):
    concatenated_data = []
    for folder_name, _, file_names in os.walk(root_folder):
        for file_name in file_names:
            if file_name == target_file:
                file_path = os.path.join(folder_name, file_name)
                concatenated_data.extend(read_data_from_file(file_path))
    return concatenated_data

def plot_histogram(data):
    plt.hist(data, bins=20, edgecolor='black')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Instructions: TEST_ONLY_DATA')
    plt.show()

def main():
    root_folder = './regression'
    target_file = 'instr_dump.txt'
    concatenated_data = concatenate_data_from_files(root_folder, target_file)

    instruction_counts = {instruction: concatenated_data.count(instruction) for instruction in INSTRUCTIONS}
    total_instructions = len(concatenated_data)
    instructions_tested = set(concatenated_data)
    percentage_tested = (len(instructions_tested) / len(INSTRUCTIONS)) * 100

    instruction_percentages = {instruction: (count / total_instructions) * 100 for instruction, count in instruction_counts.items()}

    instruction_counts_list = [(instruction, count) for instruction, count in instruction_counts.items()]
    instruction_percentages_list = [(instruction, f"{percentage:.2f}%") for instruction, percentage in instruction_percentages.items()]

    print("Instruction Frequencies:")
    print(tabulate(instruction_counts_list, headers=["Instruction", "Frequency"], tablefmt="grid"))

    print("\nInstruction Percentages:")
    print(tabulate(instruction_percentages_list, headers=["Instruction", "Percentage"], tablefmt="grid"))

    print(f"Instructions Tested: {len(instructions_tested)}/{len(INSTRUCTIONS)}")
    print(f"Percentage of Instructions Tested: {percentage_tested:.2f}%")

    plot_histogram(concatenated_data)

if __name__ == "__main__":
    main()
