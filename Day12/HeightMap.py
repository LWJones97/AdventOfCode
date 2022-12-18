class MapReader:
    def __init__(self, file_location, reversed=False):
        self.file = open(file_location, 'r')
        self.reversed = reversed

    def read_map(self):
        grid = []

        while True:
            line = self.file.readline().strip()
            if line == '':
                break
            heights = [Square(char, self.reversed) for char in line]
            grid.append(heights)

        return HeightMap(grid)


class HeightMap:
    def __init__(self, grid):
        self.grid = grid
        self.start = None
        self.set_edges()

    def set_edges(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if (j - 1) >= 0:
                    self.grid[i][j].add_edge(self.grid[i][j - 1])
                if (i - 1) >= 0:
                    self.grid[i][j].add_edge(self.grid[i - 1][j])
                if (j + 1) < len(self.grid[i]):
                    self.grid[i][j].add_edge(self.grid[i][j + 1])
                if (i + 1) < len(self.grid):
                    self.grid[i][j].add_edge(self.grid[i + 1][j])
                if self.grid[i][j].start:
                    self.start = self.grid[i][j]

    def __repr__(self):
        string = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                string = string + str(self.grid[i][j])
            string = string + '\n'
        return string


class Square:
    def __init__(self, height_char, reversed=False):
        self.reversed = reversed

        if self.reversed:
            start_char = 'E'
            end_char = 'a'
            if height_char == 'S':
                height_char = 'a'
        else:
            start_char = 'S'
            end_char = 'E'

        self.start = height_char == start_char
        self.end = height_char == end_char
        self.connected_squares = []
        if self.start:
            self.height = 0
        elif self.end:
            self.height = ord('z') - ord('a') + 1
        else:
            if self.reversed:
                self.height = abs(ord(height_char) - ord('z')) + 1
            else:
                self.height = ord(height_char) - ord('a')
        self.visited = False

    def add_edge(self, to):
        if to.height <= (self.height + 1):
            self.connected_squares.append(to)

    def mark_visited(self):
        self.visited = True

    def __repr__(self):
        if self.start:
            return "[S]"
        elif self.end:
            return "[E]"
        else:
            return "[" + str(self.height) + "]"
