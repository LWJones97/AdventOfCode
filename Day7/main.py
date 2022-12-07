import sys
from Parser import Parser

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    parser = Parser(file_location)
    filesystem = parser.construct_filesystem()

    print("The total size of folders with size less than 1000000 is " + str(filesystem.sum_with_limit(100000)))
    free_space = 70000000 - filesystem.calculate_size()
    space_to_free = 30000000 - free_space
    print("The size of the file to delete to free enough space is " + str(filesystem.find_closest_larger_than(space_to_free)))

