class SandGridReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')
        self.sand_grid = SandGrid()

    def read_grid(self):
        while True:
            line = self.file.readline().strip()
            if line == '':
                break
            coordinates = self.parse_line(line)
            self.set_occupied_squares(coordinates)
        self.sand_grid.occupied_squares.set_floor()
        return self.sand_grid

    @staticmethod
    def parse_line(line):
        coordinate_strings = line.split(" -> ")
        coordinates = [list(map(int, coordinate_string.split(","))) for coordinate_string in coordinate_strings]
        return coordinates

    def set_occupied_squares(self, coordinates):
        for i in range(len(coordinates) - 1):
            self.sand_grid.draw_occupied_line(coordinates[i][0], coordinates[i][1], coordinates[i + 1][0], coordinates[i + 1][1])


class Sand:
    def __init__(self, x, y):
        self.position = (x, y)

    def move_down(self):
        self.position = (self.position[0], self.position[1] + 1)

    def move_diagonally_left(self):
        self.position = (self.position[0] - 1, self.position[1] + 1)

    def move_diagonally_right(self):
        self.position = (self.position[0] + 1, self.position[1] + 1)


class SandGrid:
    def __init__(self):
        self.occupied_squares = OccupiedCoordinates()
        self.moving_sand = None
        self.settled_count = 0

    def next_time_step(self, infinite_void=True):
        if self.moving_sand is None:
            self.spawn_sand()
            return self.moving_sand

        current_location = self.moving_sand.position

        if self.is_square_below_empty(current_location[0], current_location[1]):
            self.moving_sand.move_down()
        elif self.is_square_diagonally_left_empty(current_location[0], current_location[1]):
            self.moving_sand.move_diagonally_left()
        elif self.is_square_diagonally_right_empty(current_location[0], current_location[1]):
            self.moving_sand.move_diagonally_right()
        else:
            self.occupied_squares.set_occupied(current_location[0], current_location[1])
            self.settled_count = self.settled_count + 1
            if current_location == (500, 0):
                return None
            self.spawn_sand()

        if infinite_void and self.occupied_squares.is_below_all_occupied(self.moving_sand.position[0], self.moving_sand.position[1]):
            return None
        else:
            return self.moving_sand

    def is_square_below_empty(self, x, y):
        return not self.occupied_squares.is_occupied(x, y + 1)

    def is_square_diagonally_left_empty(self, x, y):
        return not self.occupied_squares.is_occupied(x - 1, y + 1)

    def is_square_diagonally_right_empty(self, x, y):
        return not self.occupied_squares.is_occupied(x + 1, y + 1)

    def spawn_sand(self):
        self.moving_sand = Sand(500, 0)

    def draw_occupied_line(self, x1, y1, x2, y2):
        if not (x1 == x2 or y1 == y2):
            raise ValueError("Expecting vertical or horizontal line.")

        if x1 == x2:
            self.__draw_vertical_line(x1, y1, y2)
        else:
            self.__draw_horizontal_line(y1, x1, x2)

    def __draw_vertical_line(self, x, y1, y2):
        y_min = min(y1, y2)
        y_max = max(y1, y2)

        for y in range(y_min, y_max + 1):
            self.occupied_squares.set_occupied(x, y)

    def __draw_horizontal_line(self, y, x1, x2):
        x_min = min(x1, x2)
        x_max = max(x1, x2)

        for x in range(x_min, x_max + 1):
            self.occupied_squares.set_occupied(x, y)


class OccupiedCoordinates:
    def __init__(self):
        self.occupied_coordinates = {}
        self.max_y = None
        self.floor = None

    def set_floor(self):
        self.floor = self.max_y + 2

    def set_occupied(self, x, y):
        new_occupied = self.occupied_coordinates.get(x, set())
        new_occupied.add(y)
        self.occupied_coordinates.update({x: new_occupied})

        if self.max_y is None or y > self.max_y:
            self.max_y = y

    def is_occupied(self, x, y):
        return y in self.occupied_coordinates.get(x, set()) or y == self.floor

    def is_below_all_occupied(self, x, y):
        return y > self.max_y
