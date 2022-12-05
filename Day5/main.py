import copy
import sys
from CraneFileReader import CraneFileReader

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]
    file = CraneFileReader(file_location)

    original_stacks = file.read_stacks()
    instructions = file.read_instructions()

    stacks1 = copy.deepcopy(original_stacks)
    stacks2 = copy.deepcopy(original_stacks)

    for instruction in instructions:
        stacks1.move_one_by_one(instruction["from"], instruction["to"], instruction["move"])
        stacks2.move_together(instruction["from"], instruction["to"], instruction["move"])

    print("Resulting top crates for each stack, when moving one-by-one.")
    print(stacks1.view_top_crates())
    print("Resulting top crates for each stack, when moving in clusters.")
    print(stacks2.view_top_crates())
