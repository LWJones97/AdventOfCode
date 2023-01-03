import functools


class SensorFileReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')

    def read_sensors(self):
        sensors = []
        while True:
            line = self.file.readline().strip()
            if line == '':
                break
            locations = self.parse_line(line)
            sensors.append(Sensor(locations["sensor_location"], locations["beacon_location"]))
        return sensors

    def parse_line(self, line):
        line = line.replace("Sensor at ", "")
        line = line.replace(": closest beacon is at", "")

        coordinates = line.split(" x=")
        coordinates = [coordinate.replace("x=", "") for coordinate in coordinates]
        coordinates = [coordinate.replace("y=", "") for coordinate in coordinates]
        coordinates = [list(map(int, coordinate.split(", "))) for coordinate in coordinates]
        coordinates = [ManhattanCoordinate(coordinate[0], coordinate[1]) for coordinate in coordinates]
        return {"sensor_location": coordinates[0], "beacon_location": coordinates[1]}


@functools.total_ordering
class Range:
    def __init__(self, lower, upper):
        if (lower is None) or (upper is None) or lower > upper:
            lower = None
            upper = None
        self.lower = lower
        self.upper = upper

    def is_empty(self):
        return self.lower is None or self.upper is None

    def __repr__(self):
        return "(" + str(self.lower) + "," + str(self.upper) + ")"

    def __len__(self):
        if self.lower is None:
            return 0
        return self.upper - self.lower + 1

    def __eq__(self, other):
        if self.is_empty():
            return other.is_empty()
        else:
            return (self.lower == other.lower) and (self.upper == other.upper)

    def __le__(self, other):
        if self.is_empty():
            return True
        elif other.is_empty():
            return False
        elif self.lower == other.lower:
            return self.upper <= other.upper
        else:
            return self.lower < other.lower

    def split_range(self, split_point):
        if split_point < self.lower:
            return [Range(None, None), self]
        if split_point > self.upper:
            return [self, Range(None, None)]
        return [Range(self.lower, split_point - 1), Range(split_point + 1, self.upper)]

    def disjoint(self, other):
        if self.is_empty() or other.is_empty():
            return True
        lower_disjoint = (self.upper < other.lower)
        upper_disjoint = (self.lower > other.upper)

        return lower_disjoint or upper_disjoint

    def intersects(self, other):
        return not self.disjoint(other)

    def union(self, other):
        if self.intersects(other):
            new_lower = min(self.lower, other.lower)
            new_upper = max(self.upper, other.upper)
            return [Range(new_lower, new_upper)]

        if self.is_empty():
            if other.is_empty():
                return []
            else:
                return [other]

        if other.is_empty():
            return self

        return [self, other]


class Sensor:
    def __init__(self, sensor_coordinate, beacon_coordinate):
        self.position = sensor_coordinate
        self.closest_beacon = beacon_coordinate
        self.range = self.__get_range(beacon_coordinate)

    def __get_range(self, beacon_coordinate):
        return self.position.distance_to(beacon_coordinate)

    def get_empty_range_in_row(self, row_y):
        row_distance = abs(self.position.y - row_y)
        if row_distance > self.range:
            return Range(None, None)
        range_len = self.range - row_distance
        row_range = Range(self.position.x - range_len, self.position.x + range_len)

        if self.is_beacon_in_row(row_y):
            split_range = row_range.split_range(self.closest_beacon.x)
            if split_range[0] == Range(None, None):
                return split_range[1]
            else:
                return split_range[0]
        else:
            return row_range

    def is_beacon_in_row(self, row_y):
        return self.closest_beacon.y == row_y

    def get_perimeter(self, limit=None):
        perimeter_points = []
        for i in range(self.range):
            x_distance = i
            y_distance = self.range + 1 - i
            x_right = self.position.x + x_distance
            x_left = self.position.x - x_distance
            y_right = self.position.y + y_distance
            y_left = self.position.y - y_distance
            if limit is None or (x_right <= limit and y_right <= limit and x_right >= 0 and y_right >= 0):
                perimeter_points.append(ManhattanCoordinate(x_right, y_right))
            if limit is None or (x_right <= limit and y_left <= limit and x_right >= 0 and y_left >= 0):
                perimeter_points.append(ManhattanCoordinate(x_right, y_left))
            if limit is None or (x_left <= limit and y_right <= limit and x_left >= 0 and y_right >= 0):
                perimeter_points.append(ManhattanCoordinate(x_left, y_right))
            if limit is None or (x_left <= limit and y_left <= limit and x_left >= 0 and y_left >= 0):
                perimeter_points.append(ManhattanCoordinate(x_left, y_left))
        return perimeter_points


class ManhattanCoordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, coordinate):
        return abs(self.x - coordinate.x) + abs(self.y - coordinate.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        as_string = "(" + str(self.x) + ", " + str(self.y) + ")"
        return as_string

    def __hash__(self):
        return hash((self.x, self.y))
