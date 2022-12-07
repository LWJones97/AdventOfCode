class FileSystem:
    def __init__(self):
        self.current_directory = Directory("root", None)

    def change_directory(self, name):
        if name == "..":
            self.__go_up_one_level()
        else:
            self.__create_and_change_directory(name)

    def create_directory(self, name):
        self.current_directory.add_subdirectory(name)

    def create_file(self, name, size):
        self.current_directory.add_file(name, size)

    def reset(self):
        while self.current_directory.parent is not None:
            self.__go_up_one_level()

    def __create_and_change_directory(self, name):
        self.create_directory(name)
        self.current_directory = self.current_directory.get_subdirectory(name)

    def __go_up_one_level(self):
        self.current_directory = self.current_directory.parent

    def calculate_size(self):
        return self.current_directory.calculate_size()

    def sum_with_limit(self, limit):
        return self.current_directory.sum_with_limit(limit)

    def find_closest_larger_than(self, value):
        total_size = self.calculate_size()
        return self.current_directory.find_closest_larger_than(value, total_size)

    def __str__(self):
        return str(self.current_directory)


class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.subdirectories = dict()
        self.files = dict()
        self.parent = parent
        self.size = None

    def add_file(self, name, size):
        if name not in self.files:
            self.files[name] = File(name, size)

    def add_subdirectory(self, name):
        if name not in self.subdirectories:
            self.subdirectories[name] = Directory(name, self)

    def get_subdirectory(self, name):
        return self.subdirectories[name]

    def to_string(self, space_count=0):
        string = "  " * space_count + "* " + self.name + "\n"

        for subdirectory in self.subdirectories.values():
            string = string + subdirectory.to_string(space_count + 1)

        for file in self.files.values():
            string = string + "  " * space_count + "* " + file.name + "\n"

        return string

    def calculate_size(self):
        if self.size is not None:
            return self.size

        size = 0

        for file in self.files.values():
            size = size + file.size

        for subdirectory in self.subdirectories.values():
            size = size + subdirectory.calculate_size()

        self.size = size
        return size

    def sum_with_limit(self, limit):
        self.calculate_size()
        sum = 0
        if self.size <= limit:
            sum = sum + self.size

        for subdirectory in self.subdirectories.values():
            sum = sum + subdirectory.sum_with_limit(limit)
        return sum

    def find_closest_larger_than(self, value, current_best):
        if self.size >= value and self.size < current_best:
            current_best = self.size

        for subdirectory in self.subdirectories.values():
            subdirectory_best = subdirectory.find_closest_larger_than(value, current_best)
            if subdirectory_best < current_best:
                current_best = subdirectory_best

        return current_best


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
