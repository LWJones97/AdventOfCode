import copy


class RopeMover:
    def __init__(self, n):
        self.rope = Rope(n)
        self.visited_locations = set()
        self.update_visited()

    def update_visited(self):
        self.visited_locations.add(copy.deepcopy(self.rope.get_tail_coordinate()))

    def execute_instructions(self, file_location):
        file = open(file_location, 'r')

        while True:
            instruction = file.readline().strip()
            if instruction == '':
                break
            instruction = self.parse_instruction(instruction)
            self.move(instruction[0], instruction[1])

    def move(self, direction, n):
        if direction == 'U':
            self.move_up(n)
        elif direction == 'L':
            self.move_left(n)
        elif direction == 'R':
            self.move_right(n)
        elif direction == 'D':
            self.move_down(n)
        else:
            raise ValueError

    def move_up(self, n):
        for i in range(n):
            self.rope.move_up()
            self.update_visited()

    def move_down(self, n):
        for i in range(n):
            self.rope.move_down()
            self.update_visited()

    def move_left(self, n):
        for i in range(n):
            self.rope.move_left()
            self.update_visited()

    def move_right(self, n):
        for i in range(n):
            self.rope.move_right()
            self.update_visited()

    @staticmethod
    def parse_instruction(instruction):
        instruction = instruction.split(" ")
        instruction[1] = int(instruction[1])
        return instruction


class Rope:
    def __init__(self, n):
        self.segment_count = (n - 1)
        self.segments = []
        self.segments.append(RopeSegment(Coordinate(0, 0), Coordinate(0, 0)))
        self.head = self.segments[0]

        for i in range(self.segment_count - 1):
            self.segments.append(RopeSegment(self.segments[i].tail, Coordinate(0, 0)))

    def move_up(self):
        self.head.move_up()
        self.update_tail()

    def move_down(self):
        self.head.move_down()
        self.update_tail()

    def move_left(self):
        self.head.move_left()
        self.update_tail()

    def move_right(self):
        self.head.move_right()
        self.update_tail()

    def update_tail(self):
        for i in range(self.segment_count - 1):
            self.segments[i + 1].update_tail()

    def get_tail_coordinate(self):
        return self.segments[-1].tail


class RopeSegment:
    def __init__(self, head_coordinate, tail_coordinate):
        self.head = head_coordinate
        self.tail = tail_coordinate

    def update_tail(self):
        self.tail.move_towards(self.head)

    def move_up(self):
        self.head.move_up()
        self.update_tail()

    def move_down(self):
        self.head.move_down()
        self.update_tail()

    def move_left(self):
        self.head.move_left()
        self.update_tail()

    def move_right(self):
        self.head.move_right()
        self.update_tail()

    def __str__(self):
        printed = "Head: " + str(self.head) + "\n"
        printed = printed + "Tail: " + str(self.tail) + "\n"
        return printed


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (other.x == self.x) and (other.y == self.y)
        else:
            raise NotImplementedError

    def __hash__(self):
        return hash((self.x, self.y))

    def move_up(self):
        self.y = self.y + 1

    def move_down(self):
        self.y = self.y - 1

    def move_left(self):
        self.x = self.x - 1

    def move_right(self):
        self.x = self.x + 1

    def move_towards(self, coordinate):
        if not self.is_touching(coordinate):
            original_x = self.x
            original_y = self.y

            if coordinate.x > original_x:
                self.move_right()

            if coordinate.x < original_x:
                self.move_left()

            if coordinate.y > original_y:
                self.move_up()

            if coordinate.y < original_y:
                self.move_down()

    def is_touching(self, coordinate):
        return self.distance(coordinate) <= 1

    def distance(self, coordinate):
        return max(abs(self.x - coordinate.x), abs(self.y - coordinate.y))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"
