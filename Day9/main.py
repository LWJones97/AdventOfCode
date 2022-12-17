import sys
from RopeMover import RopeMover

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    short_rope_mover = RopeMover(2)
    short_rope_mover.execute_instructions(file_location)

    print("The number of squares visited by the tail of the short rope is "
          + str(len(short_rope_mover.visited_locations)) + ".")

    long_rope_mover = RopeMover(10)
    long_rope_mover.execute_instructions(file_location)
    print("The number of squares visited by the tail of the long rope is "
          + str(len(long_rope_mover.visited_locations)) + ".")
