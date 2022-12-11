import sys
from GridReader import GridReader

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Expected usage: main.py <path to input file>")

    file_location = sys.argv[1]

    grid = GridReader(file_location).read_grid()

    row_count = grid.get_row_count()
    column_count = grid.get_column_count()

    grid.update_visibilities()

    visible = 0
    max_scenic = 0

    for row in range(row_count):
        for column in range(column_count):
            visible = visible + int(grid.get(row, column).get_visibility())
            scenic = grid.calculate_scenic_value(row, column)

            if scenic > max_scenic:
                max_scenic = scenic

    print("The number of visible trees is " + str(visible) + ".")
    print("The maximum scenic value is " + str(max_scenic) + ".")

