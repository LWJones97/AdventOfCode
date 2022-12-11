from Tree import Tree


class Grid:
    def __init__(self):
        self.grid = []

    def get(self, row, column):
        return self.grid[row][column]

    def get_row_count(self):
        return len(self.grid)

    def get_column_count(self):
        return len(self.grid[0])

    def add_row(self, row):
        self.grid.append(row)

    def update_visibilities(self):
        self.update_column_visibilities()
        self.update_row_visibilities()

    def update_column_visibilities(self):
        column_count = len(self.grid[0])

        for column in range(column_count):
            self.update_column_visibility(column)

    def update_row_visibilities(self):
        row_count = len(self.grid)

        for row in range(row_count):
            self.update_row_visibility(row)

    def update_row_visibility(self, row):
        column_count = len(self.grid[row])
        max_height_left = -1
        max_height_right = -1
        for i in range(column_count):
            max_height_left = self.grid[row][i].update_visibility(max_height_left)
            max_height_right = self.grid[row][column_count - 1 - i].update_visibility(max_height_right)

    def update_column_visibility(self, column):
        row_count = len(self.grid)
        max_height_up = -1
        max_height_down = -1
        for i in range(row_count):
            max_height_up = self.grid[i][column].update_visibility(max_height_up)
            max_height_down = self.grid[row_count - 1 - i][column].update_visibility(max_height_down)

    def calculate_scenic_value(self, row, column):
        height = self.grid[row][column].height

        trees_left = column
        trees_right = self.get_column_count() - 1 - column
        trees_up = row
        trees_down = self.get_row_count() - 1 - row

        scenic_left = 0
        scenic_right = 0
        scenic_up = 0
        scenic_down = 0

        for i in range(trees_left):
            scenic_left = scenic_left + 1
            if self.grid[row][column - (i + 1)].height >= height:
                break

        for i in range(trees_right):
            scenic_right = scenic_right + 1
            if self.grid[row][column + (i + 1)].height >= height:
                break

        for i in range(trees_up):
            scenic_up = scenic_up + 1
            if self.grid[row - (i + 1)][column].height >= height:
                break

        for i in range(trees_down):
            scenic_down = scenic_down + 1
            if self.grid[row + (i + 1)][column].height >= height:
                break

        return scenic_down * scenic_up * scenic_right * scenic_left


class GridReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')

    def read_grid(self):
        grid = Grid()

        while True:
            values = self.file.readline().strip()
            if values == '':
                break
            digits = [Tree(int(value)) for value in values]
            grid.add_row(digits)
        return grid
