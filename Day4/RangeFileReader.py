class Range:
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def get_lower(self):
        return self.lower

    def get_upper(self):
        return self.upper

    def contains(self, range):
        return (self.lower <= range.get_lower()) and (self.upper >= range.get_upper())

    def disjoint(self, range):
        lower_disjoint = (self.upper < range.get_lower())
        upper_disjoint = (self.lower > range.get_upper())

        return lower_disjoint or upper_disjoint

    def overlaps(self, range):
        return not self.disjoint(range)


class RangeFileReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')

    def get_next_item(self):
        line = self.file.readline().strip()

        if line is '':
            return None

        ranges = line.split(',')

        return RangeFileReader.__convert_to_range(ranges[0]), RangeFileReader.__convert_to_range(ranges[1])

    @staticmethod
    def __convert_to_range(string):
        split_string = string.split('-')
        return Range(int(split_string[0]), int(split_string[1]))


