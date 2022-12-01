class CalorieFileReader:
    def __init__(self, file_location):
        self.file = open(file_location, 'r')
        self.elf = 0

    def get_next_item(self):
        while True:
            line = self.__next_line()

            if line is None:
                return None
            elif line == '':
                self.elf = self.elf + 1
            else:
                return {"calories": int(line), "elf": self.elf}

    def __next_line(self):
        line = self.file.readline()
        if line == '':
            return None

        line = self.__strip_newline(line)
        return line

    def __strip_newline(self, line):
        return line.replace('\n', '')