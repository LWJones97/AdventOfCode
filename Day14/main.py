import sys
from SandGrid import SandGridReader

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    sand_grid = SandGridReader(file_location).read_grid()

    while True:
        sand = sand_grid.next_time_step(True)
        if sand is None:
            break

    print("The total number of settled blocks in the case without a floor is " + str(sand_grid.settled_count))

    sand_grid = SandGridReader(file_location).read_grid()

    while True:
        sand = sand_grid.next_time_step(False)
        if sand is None:
            break

    print("The total number of settled blocks before the source gets blocked is " + str(sand_grid.settled_count))




